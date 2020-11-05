variable "aws_region" {
  type = string
  description = "AWS Region to Deploy lambda function to"
  default = "us-east-1"
}

variable "lambda_function_name" {
  type = string
  description = "Lambda function name, normally named after operational function"
}

variable "lambda_runtime" {
  type = string
  description = "Lambda Function Runtime Environment"
  default = "nodejs12.x"
}

variable "lambda_source_file" {
  type = string
  description = "Lambda Function Code"
}

variable "iam_attach_policy_statements" {
  type = bool
  description = "Attach IAM Policy Statements"
  default = true
}

variable "iam_policy_statement" {
  type = any
  description = "IAM Policy Definition"

}
