provider "aws" {
  profile = "default"
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------

module "hyperglance_automations" {
  source = "git::https://github.com/hyperglance/terraform-aws-hyperglance.git//modules/hyperglance-automations"

  hyperglance_automation_list    = "../../../files/HyperglanceAutomations.json"
  lambda_package = "../../../lambda"
}