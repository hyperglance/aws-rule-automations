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
# CREATE AN S3 BUCKET
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_s3_bucket" "hyperglance_automations_bucket" {
  bucket = random_pet.hyperglance_automations_name.id
  acl    = "private"
  tags   = var.tags
  force_destroy = true
}

resource "aws_s3_bucket_policy" "hyperglance_bucket_policy" {
  bucket = aws_s3_bucket.hyperglance_automations_bucket.id
  # NB. do not change the indentation in the following section
  policy = <<POLICY
{ 
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::${random_pet.hyperglance_automations_name.id}/*",
            "Condition": {
                "ArnNotEquals": {
                    "aws:PrincipalArn": [
                      "${module.automations_lambda_role.automation_role_arn}",
                      "${var.hyperglance_identity_arn}",
                      "${data.aws_caller_identity.current.arn}"
                      ]
                }
            }
        }
        ]
}
POLICY
  depends_on = [
    aws_s3_bucket_object.hyperglance_automation_list,
    aws_s3_bucket_notification.bucket_notification,
    module.automations_lambda_role
    ]
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
  program = local.is_windows ? ["py", "-3", var.generate_automations_script] : ["python3", var.generate_automations_script]
}

# ---------------------------------------------------------------------------------------------------------------------
# WHAT IS MY ACCOUNT ID? OTHER METADATA ..
# ---------------------------------------------------------------------------------------------------------------------

data "aws_caller_identity" "current" {}

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
  automation_unique_name = random_pet.hyperglance_automations_name.id
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
  timeout          = 900

  tags = var.tags
}

# ---------------------------------------------------------------------------------------------------------------------
# SUBSCRIBE THE LAMBDA TO S3 OBJECT EVENTS
# Hyperglance will create event.json files in the bucket that we need to subscribe to
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.hyperglance_automations_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.hyperglance_automations_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = "event.json"
  }

  depends_on = [aws_lambda_permission.hyperglance_automation_permissions]
}

# ---------------------------------------------------------------------------------------------------------------------
# ALLOW S3 TO TRIGGER LAMBDA EXECUTION
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_lambda_permission" "hyperglance_automation_permissions" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hyperglance_automations_lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.hyperglance_automations_bucket.arn
}