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
| aws\_region | AWS Region to Deploy Event Bridge | `string` | `"us-east-1"` | no |
| create\_event | Resource Creation Conditional | `bool` | `true` | no |
| event\_description | Event Description | `string` | `"Triggers a Lambda Function that requests the topology from Hyperglance API"` | no |
| event\_name | Event Bridge Event Name | `string` | `"HyperglanceRequestTopology"` | no |
| event\_schedule | Event Schedule, CRON or RATE expression | `string` | `"rate(1 day)"` | no |
| event\_target\_arn | Target ARN (lambda) | `string` | n/a | yes |
| target\_lambda\_name | Target Lambda Name | `string` | n/a | yes |

## Outputs

No output.
