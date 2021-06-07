## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.14.0, < 0.15 |
| archive | 2.1.0 |
| random | 3.1.0 |

## Providers

| Name | Version |
|------|---------|
| archive | 2.1.0 |
| aws | n/a |
| random | 3.1.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| hyperglance\_automation\_list | Path to Automation list used by Hyperglance | `string` | n/a | yes |
| lambda\_package | Path to lambda code | `string` | n/a | yes |
| tags | Resource Tags to Apply | `map(string)` | <pre>{<br>  "Description": "Resources Required by Hyperglance Automations",<br>  "Help": "https://support.hyperglance.com/",<br>  "Name": "Hyperglance Automations",<br>  "Persistent": "True",<br>  "Source": "https://github.com/hyperglance/aws-rule-automations"<br>}</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket\_name | The bucket name to use in Hyperglance Notification Configuration |
| topic\_arn | The SNS Topic ARN to use in Hyperglance Notification Configuration |

