output "bucket_name" {
  value       = aws_s3_bucket.hyperglance_automations_bucket.id
  description = "The bucket name to use in Hyperglance Notification Configuration"
}

output "topic_arn" {
  value       = aws_sns_topic.hyperglance_sns_topic.arn
  description = "The SNS Topic ARN to use in Hyperglance Notification Configuration"
}