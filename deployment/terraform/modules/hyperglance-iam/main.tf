
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

data "external" "policy_json" {
    program = local.is_windows ? ["py -3", var.generate_permissions_script] : ["python3", var.generate_permissions_script]
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN AWS IAM POLICY FOR automations EXECUTION
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
      },
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
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN IAM ROLE AND ATTACH DEFINED POLICIES
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role" "hyperglance_automation_role" {
  name_prefix = "Hyperglance_Automations"
  assume_role_policy = data.aws_iam_policy_document.hyperglance_automation_assume_policy.json
  managed_policy_arns = [
    aws_iam_policy.hyperglance_automation_policy.arn,
    "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  ]
  tags = var.tags
}
