output "bucket_name" {
  value       = aws_s3_bucket.hyperglance_automations_bucket.id
  description = "The bucket name to use in Hyperglance Notification Configuration"
}

output "lambda_arn" {
  value       = aws_lambda_function.hyperglance_automations_lambda.arn
  description = "The ARN of the deployed lambda function to be used in x-account deployment"
}
