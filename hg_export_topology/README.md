# Hyperglance - Export Topology to S3

This deployment contains a terraform configuration that deploys an Event Bridge, S3 Bucket and Lambda function that requests an export of the Monitored Topology to S3, by default is will do this Once Per Day, for all AWS Resources - All Options are Configurable.

Please ensure you have read the main repository [ReadMe](https://github.com/hyperglance/aws-rule-automations/blob/master/README.md) to ensure all pre-requisites are installed and configured, and you have cloned / downloaded the repository.

## Creating a Hyperglance API Key

An API Key is required, a guide is availbale [here](https://support.hyperglance.com/knowledge/getting-started-with-the-hyperglance-api)

## Usage

To deploy this, from the hg_export_topology directory and execute the following command sequence:

```bash
terraform init
terraform apply
```

Terraform will prompt you for some required parameters:

```bash
var.API_KEY
  Hyperglance API Key

  Enter a value:

var.API_KEY_NAME
  Hyperglance API Key Name

  Enter a value:

var.HYPERGLANCE_IP
  Hyperglance Instance IP or DNS Name

  Enter a value:
```

Enter the required Parameters, the deployment will fail if these are not provided.

>Note: To avoid having to set these manually, you can update the variables.tf file with default values

```terraform
variable "HYPERGLANCE_IP" {
  description = "Hyperglance Instance IP or DNS Name"
  type        = string
  default     = "YOUR_HYPERGLANCE_IP"
}
```

## Request Options

The EXPORT_DATASOURCE, EXPORT_ACCOUNT and EXPORT_ID control the request from Hyperglance, by default all AWS resources are returned:

```terraform
variable "EXPORT_DATASOURCE" {
  description = "Hyperglance Data Source"
  type = string
  default = "Datasource_Group"
}

variable "EXPORT_ACCOUNT" {
  description = "Hyperglance Account to Export"
  type        = string
  default     = "Amazon"
}

variable "EXPORT_ID" {
  description = "Hyperglance Object ID to Export"
  type        = string
  default     = "Amazon"
}
```

You can modify these parameters in `variables.tf` to request just the elements you want, here are some examples:

Export one AWS Account

```bash
EXPORT_DATASOURCE = "Amazon"
EXPORT_ACCOUNT = "My AWS"
EXPORT_ID = "account:My Aws"
```

Export an AWS VPC

```bash
EXPORT_DATASOURCE = "Amazon"
EXPORT_ACCOUNT = "My AWS"
EXPORT_ID = "vpc-987654321"
```

Export one Azure Subscription

```bash
EXPORT_DATASOURCE = "Azure"
EXPORT_ACCOUNT = "My Azure Subscription"
EXPORT_ID = "sub:My Azure Subscription"
```

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

