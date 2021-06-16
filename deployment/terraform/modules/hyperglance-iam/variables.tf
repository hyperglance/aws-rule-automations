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