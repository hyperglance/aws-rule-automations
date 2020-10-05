# Hyperglance Event Configuration

Configuration in this directory creates Lambda Function, SNS topic, and IAM Policies for EC2 Tag and Terminate.

## Pre-Rquisites

[Terraform Installed and Available from Command line](https://www.terraform.io/downloads.html)

[AWS CLI, Installed and Configured with Appropriate Credentials](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
 

## Usage

To run this you need to execute:

```bash
$ terraform init
$ terraform plan -out hg_lambda
$ terraform apply "hg_lambda"
```

Note that this example may create resources which cost money. Run `terraform destroy` when you don't need these resources.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12.6, < 0.14 |
| aws | >= 3.80, < 4.0 |
| random | ~> 2.30 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 3.80, < 4.0 |
| random | ~> 2.30 |

## Inputs

No input.

## Outputs

| Name | Description |
|------|-------------|
| lambda\_cloudwatch\_log\_group\_arn | The ARN of the Cloudwatch Log Group |
| lambda\_role\_arn | The ARN of the IAM role created for the Lambda Function |
| lambda\_role\_name | The name of the IAM role created for the Lambda Function |
| local\_filename | The filename of zip archive deployed (if deployment was from local) |
| s3\_object | The map with S3 object data of zip archive deployed (if deployment was from S3) |
| this\_lambda\_function\_arn | The ARN of the Lambda Function |
| this\_lambda\_function\_invoke\_arn | The Invoke ARN of the Lambda Function |
| this\_lambda\_function\_kms\_key\_arn | The ARN for the KMS encryption key of Lambda Function |
| this\_lambda\_function\_last\_modified | The date Lambda Function resource was last modified |
| this\_lambda\_function\_name | The name of the Lambda Function |
| this\_lambda\_function\_qualified\_arn | The ARN identifying your Lambda Function Version |
| this\_lambda\_function\_source\_code\_hash | Base64-encoded representation of raw SHA-256 sum of the zip file |
| this\_lambda\_function\_source\_code\_size | The size in bytes of the function .zip file |
| this\_lambda\_function\_version | Latest published version of Lambda Function |
| this\_lambda\_layer\_arn | The ARN of the Lambda Layer with version |
| this\_lambda\_layer\_created\_date | The date Lambda Layer resource was created |
| this\_lambda\_layer\_layer\_arn | The ARN of the Lambda Layer without version |
| this\_lambda\_layer\_source\_code\_size | The size in bytes of the Lambda Layer .zip file |
| this\_lambda\_layer\_version | The Lambda Layer version |