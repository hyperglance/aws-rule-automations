
# ---------------------------------------------------------------------------------------------------------------------
# REQUIRE A SPECIFIC TERRAFORM FAMILY
# ---------------------------------------------------------------------------------------------------------------------

terraform {
  required_version = ">= 0.13.6"
}

# ---------------------------------------------------------------------------------------------------------------------
# WE MUST BE MINDFUL OF GOVCLOUD
# ---------------------------------------------------------------------------------------------------------------------

data "aws_partition" "current" {}

# ---------------------------------------------------------------------------------------------------------------------
# IS WINDOWS?
# ---------------------------------------------------------------------------------------------------------------------

locals {
  is_windows = substr(pathexpand("~"), 0, 1) == "/" ? false : true
}

# ---------------------------------------------------------------------------------------------------------------------
# GET THE POLICIES FROM THE AVAILABLE AUTOMATIONS
# ---------------------------------------------------------------------------------------------------------------------

data "aws_arn" "lambda_arn" {
  arn=var.lambda_arn
}

data "external" "policy_json" {
    program = local.is_windows ? ["py", "-3", var.generate_permissions_script] : ["python3", var.generate_permissions_script]
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN AWS IAM POLICY FOR INDIVIDUAL AUTOMATION PERMISSIONS
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_policy" "hyperglance_automation_policy" {
  name_prefix = "Hyperglance_Automation_Policy"
  path        = "/"
  description = "Hyperglance Automations, Execution Policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = values(data.external.policy_json.result)
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN AWS IAM POLICY FOR CORE AUTOMATION PERMISSIONS
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_policy" "hyperglance_automation_core_policy" {
  name_prefix = "Hyperglance_Automation_Policy"
  path        = "/"
  description = "Hyperglance Automations, Execution Policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
          "s3:GetObject",
          "s3:PutObject"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN ASSUME ROLE POLICY, FOR LAMBDA AND X-ACCOUNT EXECUTION
# ---------------------------------------------------------------------------------------------------------------------

data "aws_iam_policy_document" "hyperglance_automation_assume_policy" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }

    principals {
      type        = "AWS"
      identifiers = ["arn:${data.aws_partition.current.partition}:iam::${data.aws_arn.lambda_arn.account}:role/${split(":", data.aws_arn.lambda_arn.resource)[1]}"]
    }

  }
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN IAM ROLE AND ATTACH DEFINED POLICIES
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role" "hyperglance_automation_role" {
  name               = "${split(":", data.aws_arn.lambda_arn.resource)[1]}-x-account"
  assume_role_policy = data.aws_iam_policy_document.hyperglance_automation_assume_policy.json
  managed_policy_arns = [
    aws_iam_policy.hyperglance_automation_policy.arn,
    aws_iam_policy.hyperglance_automation_core_policy.arn
  ]
  tags = var.tags
}