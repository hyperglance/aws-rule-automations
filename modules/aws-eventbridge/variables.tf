variable "create_event" {
  type        = bool
  description = "Resource Creation Conditional"
  default     = true
}

variable "event_name" {
  type        = string
  description = "Event Bridge Event Name"
  default     = "hyperglanceRequestTopology"
}

variable "event_description" {
  type        = string
  description = "Event Description"
  default     = "Triggers a Lambda Function that request the topology from Hyperglance API"
}

variable "event_schedule" {
  type        = string
  description = "Event Schedule, CRON or RATE expression"
  default     = "cron(0 20 * * ? *)"
}

variable "event_target_arn" {
  type        = string
  description = "Target ARN (lambda)"
}