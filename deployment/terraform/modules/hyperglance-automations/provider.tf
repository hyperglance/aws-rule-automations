# ---------------------------------------------------------------------------------------------------------------------
# REWUIRE A SPECIFIC TERRAFORM FAMILY
# ---------------------------------------------------------------------------------------------------------------------

terraform {
  required_version = ">= 0.14.0, < 0.15"

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "2.1.0"
    }

  }
}