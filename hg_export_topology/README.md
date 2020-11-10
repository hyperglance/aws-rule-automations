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
| API\_KEY | Hyperglance API Key | `string` | n/a | yes |
| API\_KEY\_NAME | Hyperglance API Key Name | `string` | n/a | yes |
| EXPORT\_ACCOUNT | Hyperglance Account to Export | `string` | `"Amazon"` | no |
| EXPORT\_ID | Hyperglance Object ID to Export | `string` | `"Amazon"` | no |
| HYPERGLANCE\_IP | Hyperglance Instance IP or DNS Name | `string` | n/a | yes |
| aws\_region | AWS Region to Deploy Event Bridge | `string` | `"us-east-1"` | no |

## Outputs

No output.

