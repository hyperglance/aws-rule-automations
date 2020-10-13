<img src="files/files/b5dfbb6c-75c8-493b-8c5d-d68b3272cf0f.png" alt="Hyperglance Logo" />

# Hyperglance Rules - Lambda Configuration

This Repository contains terrafom configurations, that deploys an SNS Topic and lambda function that can be used to remediate infrastructure, based on rules configured in [Hyperglance](https://support.hyperglance.com/knowledge/rules-dashboard-view).

:information_source: The deployed functions will only perform actions against resources in the same account, where the function is deployed.

## Pre-Requisites

Please follow the below steps to install the pre-requisites required to deploy the infrastructure.

### Install Terraform

Method 1, Select your operating system from the link below, install terraform, and add it to your `PATH`

[Terraform Installed and Available from Command line](https://www.terraform.io/downloads.html)

Method 2, Use homebrew (MAC OS / Linux), chocolately (Windows):

[Homebrew](https://brew.sh/):

`brew install terraform`

[Chocolately](https://chocolatey.org/):

`choco install terraform`

> Note: Method 2 takes care of updating your PATH variables and installing any required dependencies

Check Terraform is installed correctly:

```bash
$ terraform -version

Output:
+ terraform -version
Terraform v0.13.2
```

### Install AWS CLI

Use the follow User Guide to install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html), s elect your operating system from the appropriate topic.

Once the CLI is installed, [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) it using `aws configure` :

```bash
aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: yaml
```

> Note: The above Access and Secrets are examples, only. Please substitute the values that are appropriate for your environement.

### Clone / Download the repository:

Clone the repository:

```bash
$ mkdir code && cd code
$ git clone https://github.com/hyperglance/aws-terraform-lambda.git
```

Download the [Zip]() release, and extract it.

## Usage

To run this, from the directoryof the function you want to deploy i.e. `cd ec2_stop_instance` you need to execute the following command sequence:

```bash
$ terraform init
$ terraform apply
```

This will ask you to confirm deployment, type `yes` to confirm. You can skip confirmation using `terraform apply -auto-approve`

Once complete, the ARN of the SNS Topic will be returned:

```bash
Apply complete! Resources: 13 added, 0 changed, 0 destroyed.

Outputs:

hyperglance_sns_topic_arn = arn:aws:sns:us-east-1:0123456789987:hyperglance_ec2_tag_instance20201013101838932900000001
```
Copy everything after the equals `=` and paste it into the ["Notify AWS SNS - Topic ARN"](https://support.hyperglance.com/knowledge/rules-dashboard-view)

>Note: that this may create resources which cost money. Run `terraform destroy` when you don't need these resources.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12.6, < 0.14 |
| aws | >= 3.80, < 4.0 |
| random | ~> 2.30 |

## Inputs

The following inputs are acccepted, these can be set in `main.tf` of the appropriate function.

| Name | Description | Default | Mandatory |
|------|-------------|---------|-----------|
| aws_region | AWS Region to Deploy to | us-east-1 | Y |
| lambda_function_name | Name of Lambda Function | Function Folder Name | Y |
| lambda_runtime | Lambda execution environment | nodejs12.x | Y |
| iam_attach_policy_statements | Attach inline policies | true | N |
| iam_policy_statement | Policy Definition if iam_attach_policy_statements is true | NONE | N |

>Note: All appropriate paramters are set, you may wish to override the default aws_region.

## Outputs

| Name | Description |
|------|-------------|
| hyperglance_sns_topic_arn | The ARN of the Hyperglance SNS Topic |