terraform {
  required_version = ">= 0.12.6, < 0.14"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.8.0, < 4.0"
    }
  }
}