resource "random_pet" "this" {
  length = 2
}

module "lambda_function" {

  source  = "terraform-aws-modules/lambda/aws"
  version = "1.24.0"

  function_name = var.lambda_function_name
  handler       = "${var.lambda_function_name}.handler"
  runtime       = var.lambda_runtime

  source_path = "../functions/${var.lambda_source_file}"

  create_async_event_config = false
  attach_async_event_policy = false
  create_layer              = false

  maximum_event_age_in_seconds = 100
  maximum_retry_attempts       = 1

  environment_variables = var.environment_variables

  attach_policy_statements = var.iam_attach_policy_statements
  policy_statements        = var.iam_policy_statement
}

resource "aws_sns_topic" "hyperglance" {
  name_prefix = var.lambda_function_name
  count       = var.create_sns ? 1 : 0
}

resource "aws_lambda_permission" "with_sns" {
  statement_id  = "AllowedExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.this_lambda_function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.hyperglance[0].arn
  count         = var.create_sns ? 1 : 0
}

resource "aws_sns_topic_subscription" "topic_hyperglance" {
  topic_arn = aws_sns_topic.hyperglance[0].arn
  protocol  = "lambda"
  endpoint  = module.lambda_function.this_lambda_function_arn
  count     = var.create_sns ? 1 : 0
}