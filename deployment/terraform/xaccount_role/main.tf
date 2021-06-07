provider "aws" {
  profile = "default"
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY HYPERGLANCE AUTOMATION ROLE TO ANOTHER ACCOUNT
# ---------------------------------------------------------------------------------------------------------------------

module "hyperglance_automations_xaccount" {
  source = "../modules/hyperglance-iam-xaccount"

  ## Account ID where the Automation Lambda is located, this is to allow Assume Role
  lambda_account_id = "0123456789"

}