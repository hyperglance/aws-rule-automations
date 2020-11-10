provider "aws" {
  region = var.aws_region

  # Make it faster by skipping something
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}


resource "aws_cloudwatch_event_rule" "hg_event_rule" {
  name                = var.event_name
  description         = var.event_description
  schedule_expression = var.event_schedule
  count               = var.create_event ? 1 : 0
}

resource "aws_cloudwatch_event_target" "hg_event_target" {
  rule  = element(concat(aws_cloudwatch_event_rule.hg_event_rule.*.name, [""]), 0)
  arn   = var.event_target_arn
  count = var.create_event ? 1 : 0
}

resource "aws_lambda_permission" "hg_eventbridge" {
  statement_id  = "AllowedExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.target_lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.hg_event_rule[0].arn
  count         = var.create_event ? 1 : 0
}