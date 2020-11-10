provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

module "s3_deploy" {
  source = "../modules/aws-s3"

  bucket_name = "hyperglance-topology"
}

module "lambda_deploy" {
  source = "../modules/aws-lambda"

  create_sns = false

  lambda_function_name = "hyperglance_export_topology"
  lambda_source_file   = "hyperglance_export_topology.py"
  lambda_runtime       = "python3.8"

  iam_policy_statement = {
    s3_write = {
      effect    = "Allow",
      actions   = ["s3:PutObject", "kms:Decrypt"],
      resources = ["${module.s3_deploy.this_bucket_arn}/*", "arn:aws:kms:*:${data.aws_caller_identity.current.account_id}:key/*"]
    }
  }

  environment_variables = {
    API_KEY        = var.API_KEY,
    API_KEY_NAME   = var.API_KEY_NAME,
    BUCKET_NAME    = module.s3_deploy.this_bucket_name,
    EXPORT_ACCOUNT = var.EXPORT_ACCOUNT,
    EXPORT_ID      = var.EXPORT_ID,
    HYPERGLANCE_IP = var.HYPERGLANCE_IP
  }

}

module "eventBridge_deploy" {
  source = "../modules/aws-eventbridge"

  event_target_arn   = module.lambda_deploy.this_lambda_function_arn
  target_lambda_name = module.lambda_deploy.this_lambda_function_name
}