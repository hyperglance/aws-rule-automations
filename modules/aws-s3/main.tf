resource "aws_s3_bucket" "hg_s3_bucket" {
  name  = var.bucket_name
  acl   = "private"
  count = var.create_bucket ? 1 : 0
}