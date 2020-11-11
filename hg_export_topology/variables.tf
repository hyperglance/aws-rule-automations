variable "aws_region" {
  type        = string
  description = "AWS Region to Deploy Event Bridge"
  default     = "us-east-1"
}

variable "API_KEY" {
  description = "Hyperglance API Key - https://support.hyperglance.com/knowledge/getting-started-with-the-hyperglance-api"
  type        = string
}

variable "API_KEY_NAME" {
  description = "Hyperglance API Key Name"
  type        = string
}

variable "EXPORT_DATASOURCE" {
  description = "Hyperglance Data Source"
  type        = string
  default     = "Datasource_Group"
}

variable "EXPORT_ACCOUNT" {
  description = "Hyperglance Account to Export"
  type        = string
  default     = "Amazon"
}

variable "EXPORT_ID" {
  description = "Hyperglance Object ID to Export"
  type        = string
  default     = "Amazon"
}

variable "HYPERGLANCE_IP" {
  description = "Hyperglance Instance IP or DNS Name"
  type        = string
}