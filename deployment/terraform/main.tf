provider "aws" {
  region = "us-east-1"
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE ACTION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------

module "hyperglance_automations" {
  source = "git@github.com:hyperglance/terraform-aws-hyperglance.git//modules/hyperglance-automations"

  automation_list_source    = "../../.payloads/HyperglanceAutomations.json"
  function_payload_path = "../../lambda/Hyperglance_Automations.zip"
}