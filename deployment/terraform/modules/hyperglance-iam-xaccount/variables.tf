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

variable "lambda_account_id" {
  type        = string
  description = "Account ID of the AWS Account where the automation lamnda is deployed"
}

variable "generate_permissions_script" {
  type        = string
  description = "The script used to generate an aggregated list of the permissions needed for each automation"
}

variable "automation_unique_name" {
  type        = string
  description = "The unique name used for the hyperglance automation entities"
}