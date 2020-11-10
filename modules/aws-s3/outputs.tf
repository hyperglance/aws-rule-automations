output "this_bucket_arn" {
  value = element(concat(aws_s3_bucket.hg_s3_bucket.*.arn, [""]), 0)
}

output "this_bucket_name" {
  value = element(concat(aws_s3_bucket.hg_s3_bucket.*.id, [""]), 0)
}