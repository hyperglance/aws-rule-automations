variable "tags" {
  type        = map(string)
  description = "Resource Tags to Apply"
  default = {
    Name        = "Hyperglance Automations"
    Persistent  = "True"
    Description = "Resource Required by Hyperglance Automations"
    Help        = "https://support.hyperglance.com/"
    Source      = "https://github.com/hyperglance/aws-rule-automations"
  }
}

variable "generate_permissions_script" {
  type        = string
  description = "Path to permissions json generator"
}

variable "automation_unique_name" {
  type        = string
  description = "The random pet name prefixed with hyperglance-automations used in the automation naming convention"
}