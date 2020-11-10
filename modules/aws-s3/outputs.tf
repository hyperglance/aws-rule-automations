output "this_bucket_arn" {
  value = aws_s3_bucket.hg_s3_bucket.arn
}

output "this_bucket_name" {
  value = aws_s3_bucket.hg_s3_bucket.id
}