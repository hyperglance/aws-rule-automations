terraform {
  required_version = ">= 0.13.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.29.0, < 4.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}