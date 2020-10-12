module "lambda_deploy" {
  source = "../lambda_module"

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