provider "aws" {
  region = var.aws_region

  # Make it faster by skipping some things
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

module "lambda_deploy" {
  source = "../modules/aws-lambda"

  lambda_function_name = "hyperglance_ec2_tag_instance"
  lambda_source_file   = "hyperglance_ec2_tag_instance.js"
  iam_policy_statement = {
    ec2 = {
      effect    = "Allow",
      actions   = ["ec2:CreateTags"],
      resources = ["arn:aws:ec2:*:*:instance/*"]
    }
  }
}