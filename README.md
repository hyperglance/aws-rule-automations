<img src="https://github.com/hyperglance/aws-rule-automations/blob/master/files/b5dfbb6c-75c8-493b-8c5d-d68b3272cf0f.png" alt="Hyperglance Logo" />

![Pylint](https://github.com/hyperglance/aws-rule-automations/workflows/Pylint/badge.svg)

# Hyperglance Rule Automations - Lambda Configuration

This Repository contains terrafom configurations, that deploys an SNS Topic and lambda function that can be used to remediate infrastructure, based on rules configured in [Hyperglance](https://support.hyperglance.com/knowledge/rules-dashboard-view).

## Pre-Requisites

Please follow the below steps to install the pre-requisites required to deploy the infrastructure.

### Update Hyperglance Instance IAM Role

The policy attached to the IAM role for the Hyperglance EC2 Instance, requires the following permissions to be added:

```json
s3:PutObject,
sns:Publish
```

[AWS Policy Management - User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-edit.html)

### Install Terraform

> Note: Version 0.15 and newer is currently unsupported, use a version between 0.13.6 and 0.14.10

Method 1, Select your operating system from the link below, install terraform, and add it to your `PATH`

[Terraform Installed and Available from Command line](https://www.terraform.io/downloads.html)

[Version 0.14.10 Download](https://releases.hashicorp.com/terraform/0.14.10/)

Method 2, Use homebrew (MAC OS / Linux), chocolately (Windows):

[Homebrew](https://brew.sh/):

`brew install terraform@0.13`

[Chocolately](https://chocolatey.org/):

`choco install terraform --version 0.14.10`

> Note: Method 2 takes care of updating your PATH variables and installing any required dependencies

Check Terraform is installed correctly:

```bash
$ terraform -version

Output:
+ terraform -version
Terraform v0.13.6
```

### Install AWS CLI

Use the follow User Guide to install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html), s elect your operating system from the appropriate topic.

Once the CLI is installed, [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) it using `aws configure` :

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
```

> Note: The above Access and Secrets are examples, only. Please substitute the values that are appropriate for your environement.

Alternatively, credentials can be provided in the terraform file, or managed by [Leapp](https://github.com/Noovolari/leapp) or similar.

### Clone / Download the repository:

Clone the repository:

```bash
$ mkdir code && cd code
$ git clone https://github.com/hyperglance/aws-rule-automations.git
```

Download the [Zip](https://github.com/hyperglance/aws-rule-automations/archive/refs/tags/v2.1-beta.zip) release, and extract it.

## Usage

>OPTIONAL: To use the same region as configured using aws configure, run the following command:

```bash
export AWS_DEFAULT_REGION=$(aws configure get region --profile default)
```

Otherwise the deployment will ask you for the region:

```bash
+ terraform plan
provider.aws.region
  The region where AWS operations will take place. Examples
  are us-east-1, us-west-2, etc.

  Enter a value: 
```

To deploy the automation stack, from the `deployment/terraform/automations` directory execute the following command sequence:

```bash
$ terraform init
$ terraform apply
```

This will ask you to confirm deployment, type `yes` to confirm. You can skip confirmation using `terraform apply -auto-approve`

Once complete, the bucket name and Topic ARN required by Hyperglance will be returned:

```bash
Apply complete! Resources: 8 added, 0 changed, 0 destroyed.

Outputs:

bucket_name = "hyperglance-automations-lucky-marmoset"
topic_arn = "arn:aws:sns:us-east-1:001234567891011:hyperglance-automations-lucky-marmoset"
```

Copy these to the Notification configuration page

### Cross Account

If you plan to execute Automations on any other account, that is not the one you have deployed the stack to, you will need to deploy the role to each account

An example of the x-account role deployment, can be found in `deployment/terraform/xaccount_role` if you have more than one target account, it is best to copy this folder and rename it with the account name, to keep the state seperate.

>Note: Please ensure to update the `lambda_account_id` parameter with a valid AWS Account ID, where the the Automation lambda is located, otherwise x-account automations may fail.

When ready, execute:

```bash
$ terraform init
$ terraform apply
```

>Note: terraform will create resources which cost money. Run `terraform destroy` when you don't need these resources.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12.6, < 0.14 |
| aws | >= 3.80, < 4.0 |
| random | ~> 2.30 |

## Outputs

| Name | Description |
|------|-------------|
| topic_arn | The ARN of the Hyperglance SNS Topic |
| bucket_name | The bucket name where Automation Payloads will be delievered |