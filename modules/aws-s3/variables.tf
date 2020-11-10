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