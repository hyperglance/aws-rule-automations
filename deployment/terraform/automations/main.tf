provider "aws" {
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------


module "hyperglance_automations" {
  source = "../modules/hyperglance-automations"
  generate_permissions_script = "../../../lambda/metadata/generate_permissions_json.py"
  lambda_package = "../../../lambda"
  generate_automations_script = "../../../lambda/metadata/generate_automations_json.py"
}




