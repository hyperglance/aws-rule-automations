# ---------------------------------------------------------------------------------------------------------------------
# CREATE A RANDOM NAME GENERATOR TO USE AS THE BUCKET NAME SUFFIX
# ---------------------------------------------------------------------------------------------------------------------

resource "random_pet" "hyperglance_automations_name" {
  length    = 2
  prefix    = "hyperglance-automations"
  separator = "-"
}

# ---------------------------------------------------------------------------------------------------------------------
# GET THE LATEST LAMBDA CODE FROM GITHUB
# ---------------------------------------------------------------------------------------------------------------------

data "archive_file" "hyperglance_automations_release" {
  type        = "zip"
  source_dir  = var.lambda_package
  output_path = "Hyperglance_Automations_Lambda.zip"
}

# ---------------------------------------------------------------------------------------------------------------------
# GENERATE THE HYPERGLANCE AUTOMATIONS JSON
#----------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN S3 BUCKET
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_s3_bucket" "hyperglance_automations_bucket" {
  bucket = random_pet.hyperglance_automations_name.id
  acl    = "private"
  tags   = var.tags
  force_destroy = true
}

# ---------------------------------------------------------------------------------------------------------------------
# IS WINDOWS?
# ---------------------------------------------------------------------------------------------------------------------

locals {
  is_windows = substr(pathexpand("~"), 0, 1) == "/" ? false : true
}

# ---------------------------------------------------------------------------------------------------------------------
# GENERATE THE HYPERGLANCE AUTOMATIONS JSON
#----------------------------------------------------------------------------------------------------------------------
data "external" "hyperglance_automations_json" {
  program = local.is_windows ? ["py -3", var.generate_automations_script] : ["python3", var.generate_automations_script]
}

# ---------------------------------------------------------------------------------------------------------------------
# UPLOAD ACTION LIST TO THE S3 BUCKET
# ---------------------------------------------------------------------------------------------------------------------



resource "aws_s3_bucket_object" "hyperglance_automation_list" {
  bucket = aws_s3_bucket.hyperglance_automations_bucket.id
  key    = "HyperglanceAutomations.json"
  source = data.external.hyperglance_automations_json.result["automation_file"]
  etag   = filemd5(data.external.hyperglance_automations_json.result["automation_file"])

}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE THE LAMBDA EXECUTION ROLE
# ---------------------------------------------------------------------------------------------------------------------

module "automations_lambda_role" {
  source = "../hyperglance-iam"
  generate_permissions_script = var.generate_permissions_script
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE LAMBDA FUNCTION AND UPLOAD CODE
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_lambda_function" "hyperglance_automations_lambda" {
  function_name    = random_pet.hyperglance_automations_name.id
  filename         = "Hyperglance_Automations_Lambda.zip"
  role             = module.automations_lambda_role.automation_role_arn
  handler          = "index.lambda_handler"
  source_code_hash = data.archive_file.hyperglance_automations_release.output_base64sha256
  runtime          = "python3.8"
  timeout          = 120

  tags = var.tags
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE SNS TOPIC
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_sns_topic" "hyperglance_sns_topic" {
  name = random_pet.hyperglance_automations_name.id
  tags = var.tags
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE SNS SUBSCRIPTUON AND TRIGGER LAMBDA
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_sns_topic_subscription" "hyperglance_sns_topic_subscription" {
  topic_arn = aws_sns_topic.hyperglance_sns_topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.hyperglance_automations_lambda.arn
}

# ---------------------------------------------------------------------------------------------------------------------
# ALLOW SNS TO TRIGGER LAMBDA EXECUTION
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_lambda_permission" "hyperglance_automation_permissions" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hyperglance_automations_lambda.arn
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.hyperglance_sns_topic.arn
}