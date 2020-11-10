variable "aws_region" {
  type        = string
  description = "AWS Region to Deploy Event Bridge"
  default     = "us-east-1"
}

variable "create_event" {
  type        = bool
  description = "Resource Creation Conditional"
  default     = true
}

variable "event_name" {
  type        = string
  description = "Event Bridge Event Name"
  default     = "HyperglanceRequestTopology"
}

variable "event_description" {
  type        = string
  description = "Event Description"
  default     = "Triggers a Lambda Function that requests the topology from Hyperglance API"
}

variable "event_schedule" {
  type        = string
  description = "Event Schedule, CRON or RATE expression"
  default     = "rate(1 day)"
}

variable "event_target_arn" {
  type        = string
  description = "Target ARN (lambda)"
}

variable "target_lambda_name" {
  type        = string
  description = "Target Lambda Name"
}