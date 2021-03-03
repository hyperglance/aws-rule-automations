provider "aws" {
  region = "us-east-1"
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE ACTION RESOURCES
# ---------------------------------------------------------------------------------------------------------------------

module "hyperglance_actions" {
  source = "git@github.com:hyperglance/terraform-aws-hyperglance.git//modules/hyperglance-actions"

  action_list_source    = "../../.payloads/HGRemediationActions.json"
  function_payload_path = "../../lambda/Hyperglance_Actions.zip"
}