variable "tags" {
  type        = map(string)
  description = "Resource Tags to Apply"
  default = {
    Name        = "Hyperglance Automations"
    Persistent  = "True"
    Description = "Resources Required by Hyperglance Automations"
    Help        = "https://support.hyperglance.com/"
    Source      = "https://github.com/hyperglance/aws-rule-automations"
  }
}

variable "hyperglance_automation_list" {
  type        = string
  description = "Path to Automation list used by Hyperglance"
}

variable "lambda_package" {
  type        = string
  description = "Path to lambda code"
}
