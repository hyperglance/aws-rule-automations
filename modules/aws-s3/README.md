## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12.6, < 0.14 |
| aws | >= 3.8.0, < 4.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 3.8.0, < 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| aws\_region | AWS Region to Deploy Bucket to | `string` | `"us-east-1"` | no |
| bucket\_name | S3 Bucket Name | `string` | `"hyperglance_topology"` | no |
| create\_bucket | Resource Creation Conditional | `bool` | `true` | no |

## Outputs

| Name | Description |
|------|-------------|
| this\_bucket\_arn | n/a |
| this\_bucket\_name | n/a |
