provider "aws" {
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------


module "hyperglance_automations" {
  source = "../modules/hyperglance-automations"
  generate_permissions_script = "../../metadata/generate_permissions_json.py"
  src_package = "../../../src"
  generate_automations_script = "../../metadata/generate_automations_json.py"
}




