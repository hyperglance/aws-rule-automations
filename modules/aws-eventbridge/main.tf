resource "aws_cloudwatch_event_rule" "hg_event_rule" {
  name        = var.event_name
  description = var.event_description
  schedule    = var.event_schedule
  count       = var.create_event ? 1 : 0
}

resource "aws_cloudwatch_event_target" "hg_event_target" {
  rule  = aws_cloudwatch_event_rule.hg_event_rule.name
  arn   = var.event_target_arn
  count = var.create_event ? 1 : 0
}