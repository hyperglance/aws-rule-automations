provider "aws" {
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------


module "hyperglance_automations" {
  source = "../modules/hyperglance-automations"

  lambda_package = "../../../lambda"
  generate_automations_script = "../../../lambda/processing/automation_list.py"
}




