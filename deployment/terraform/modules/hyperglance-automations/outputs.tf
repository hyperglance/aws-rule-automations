output "bucket_name" {
  value       = aws_s3_bucket.hyperglance_automations_bucket.id
  description = "The bucket name to use in Hyperglance Notification Configuration"
}
