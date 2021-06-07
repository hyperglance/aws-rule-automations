## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.14.0, < 0.15 |

## Providers

| Name | Version |
|------|---------|
| aws | n/a |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| lambda\_account\_id | Account ID of the AWS Account where the automation lamnda is deployed | `string` | n/a | yes |
| tags | Resource Tags to Apply | `map(string)` | <pre>{<br>  "Description": "Resource Required by Hyperglance Automations",<br>  "Help": "https://support.hyperglance.com/",<br>  "Name": "Hyperglance Automations",<br>  "Persistent": "True",<br>  "Source": "https://github.com/hyperglance/aws-rule-automations"<br>}</pre> | no |

## Outputs

No output.

