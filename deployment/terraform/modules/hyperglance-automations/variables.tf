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

variable "lambda_package" {
  type        = string
  description = "Path to lambda code"
}

variable "generate_automations_script" {
  type        = string
  description = "Path to HyperglanceAutomations.json generator"
}

variable "generate_permissions_script" {
  type        = string
  description = "Path to permissions json generator"
}

variable "hyperglance_identity_arn" {
  type        = string
  description = "The arn of the identity under which hyperglance runs" 
}