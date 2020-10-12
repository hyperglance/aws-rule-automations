output "hyperglance_sns_topic_arn" {
  description = "The ARN of the SNS Topic for use in Hyperglance"
  value       = module.lambda_deploy.hyperglance_sns_topic_arn
}