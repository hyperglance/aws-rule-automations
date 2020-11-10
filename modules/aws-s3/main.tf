provider "aws" {
  region = var.aws_region

  # Make it faster by skipping something
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

resource "aws_s3_bucket" "hg_s3_bucket" {
  bucket = var.bucket_name
  acl    = "private"
  count  = var.create_bucket ? 1 : 0
}