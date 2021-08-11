provider "aws" {
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------

module "hyperglance_automations" {
  source = "../modules/hyperglance-automations"

  hyperglance_automation_list    = "../../../files/HyperglanceAutomations.json"
  lambda_package = "../../../lambda"
  generate_automations_script = "../../../lambda/processing/automation_list.py"
}
