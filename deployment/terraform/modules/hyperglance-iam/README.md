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
| tags | Resource Tags to Apply | `map(string)` | <pre>{<br>  "Description": "Resource Required by Hyperglance Automations",<br>  "Help": "https://support.hyperglance.com/",<br>  "Name": "Hyperglance Automations",<br>  "Persistent": "True",<br>  "Source": "https://github.com/hyperglance/aws-rule-automations"<br>}</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| automation\_role\_arn | n/a |

