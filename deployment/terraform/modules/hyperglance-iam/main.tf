
# ---------------------------------------------------------------------------------------------------------------------
# REQUIRE A SPECIFIC TERRAFORM FAMILY
# ---------------------------------------------------------------------------------------------------------------------

terraform {
  required_version = ">= 0.14.0, < 0.15"
}

# ---------------------------------------------------------------------------------------------------------------------
# WE MUST BE MINDFUL OF GOVCLOUD
# ---------------------------------------------------------------------------------------------------------------------

data "aws_partition" "current" {}

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
        Action = [
          "dynamodb:DeleteTable",
          "ec2:AuthorizeSecurityGroupEgress",
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:CreateSecurityGroup",
          "ec2:CreateSnapshots",
          "ec2:CreateTags",
          "ec2:DeleteSecurityGroup",
          "ec2:DeleteInternetGateway",
          "ec2:DeleteKeyPair",
          "ec2:DeleteNatGateway",
          "ec2:DeleteSnapshot",
          "ec2:DeleteTags",
          "ec2:DeleteVolume",
          "ec2:DetachInternetGateway",
          "ec2:DescribeAddresses",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeInstances",
          "ec2:DescribeVolumes",
          "ec2:DescribeVolumeStatus",
          "ec2:DescribeSnapshots",
          "ec2:DisassociateAddress",
          "ec2:ModifyInstanceAttribute",
          "ec2:ModifyImageAttribute",
          "ec2:ReleaseAddress",
          "ec2:RevokeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupIngress",
          "ec2:StopInstances",
          "ec2:TerminateInstances",
          "kms:CreateAlias",
          "kms:CreateKey",
          "kms:EnableKeyRotation",
          "iam:AttachRolePolicy",
          "iam:AttachUserPolicy",
          "iam:DetachRolePolicy",
          "iam:CreatePolicy",
          "iam:CreateRole",
          "iam:GetPolicy",
          "iam:GetUser",
          "iam:PassRole",
          "iam:ListInstanceProfilesForRole",
          "iam:UpdateAccountPasswordPolicy",
          "iam:UpdateLoginProfile",
          "elasticloadbalancing:DeleteLoadBalancer",
          "rds:DeleteDBInstance",
          "rds:ModifyDBInstance",
          "redshift:DeleteCluster",
          "s3:CreateBucket",
          "s3:DeleteBucket",
          "s3:DeleteBucketPolicy",
          "s3:GetBucketAcl",
          "s3:GetBucketPolicy",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutBucketAcl",
          "s3:PutBucketLogging",
          "s3:PutBucketPolicy",
          "s3:PutBucketVersioning",
          "s3:PutEncryptionConfiguration",
          "s3:PutBucketPublicAccessBlock",
          "s3:PutObject",
          "sts:AssumeRole",
          "sts:GetCallerIdentity",
          "workspaces:StopWorkspaces",
          "workspaces:TerminateWorkspaces"
        ]
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
