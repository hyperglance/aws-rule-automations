module "lambda_deploy" {
  source = "../modules/aws-lambda"

  lambda_function_name = "hyperglance_ec2_stop_instance"
  lambda_source_file   = "hyperglance_ec2_stop_instance.js"
  iam_policy_statement = {
    ec2 = {
      effect    = "Allow",
      actions   = ["ec2:StopInstances"],
      resources = ["arn:aws:ec2:*:*:instance/*"]
    }
  }
}