variable "aws_region" {
  type        = string
  description = "AWS Region to Deploy Bucket to"
  default     = "us-east-1"
}

variable "create_bucket" {
  type        = bool
  description = "Resource Creation Conditional"
  default     = true
}

variable "bucket_name" {
  type        = string
  description = "S3 Bucket Name"
  default     = "hyperglance_topology"
}