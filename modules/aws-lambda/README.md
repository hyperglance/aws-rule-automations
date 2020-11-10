## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12.6, < 0.14 |
| aws | >= 3.8.0, < 4.0 |
| random | ~> 2.3.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 3.8.0, < 4.0 |
| random | ~> 2.3.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| aws\_region | AWS Region to Deploy lambda function to | `string` | `"us-east-1"` | no |
| create\_sns | Create SNS Conditional | `bool` | `true` | no |
| environment\_variables | Map of Environemnt Variables | `map(string)` | `{}` | no |
| iam\_attach\_policy\_statements | Attach IAM Policy Statements | `bool` | `true` | no |
| iam\_policy\_statement | IAM Policy Definition | `any` | n/a | yes |
| lambda\_function\_name | Lambda function name, normally named after operational function | `string` | n/a | yes |
| lambda\_runtime | Lambda Function Runtime Environment | `string` | `"nodejs12.x"` | no |
| lambda\_source\_file | Lambda Function Code | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| hyperglance\_sns\_topic\_arn | The ARN of the SNS Topic for use in Hyperglance |
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
