provider "aws" {
  profile = "default"
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION ROLE TO ANOTHER ACCOUNT
# ---------------------------------------------------------------------------------------------------------------------

module "hyperglance_automations_xaccount" {
  source = "../modules/hyperglance-iam-xaccount"

  ## Account ID where the Automation Lambda is located, this is to allow Assume Role
  generate_permissions_script = "../../metadata/generate_permissions_json.py"
  lambda_arn = "arn:aws:lambda:us-east-1:005356411402:function:hyperglance-automations-solid-caribou"
}