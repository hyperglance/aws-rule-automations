<img src="https://github.com/hyperglance/aws-rule-automations/blob/master/files/b5dfbb6c-75c8-493b-8c5d-d68b3272cf0f.png" alt="Hyperglance Logo" />

# Hyperglance Rule Automations for AWS

> Enable Hyperglance to automate, fix and optimize your cloud.

This repository contains terraform configurations, that deploy an S3 Bucket and Lambda function that you connect with your Hyperglance EC2 Instance. Giving you the power to automate your cloud and fix configuration issues quickly & easily.

## Pre-Requisites

Before you can deploy automations you will need:
1. Terraform CLI - [Install instructions](https://learn.hashicorp.com/tutorials/terraform/install-cli)
2. AWS CLI - [Install instructions](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
3. IAM permissions configured on the Hyperglance Instance - See below.

### IAM Permissions

The IAM Policy on the Role associated with the Hyperglance EC2 Instance will need the following permissions added:

```json
"s3:PutObject",
"s3:GetObject",
"s3:ListBucket",
```

## Quick Start

1. Follow the pre-requisite steps above.
2. Connect the AWS CLI to the AWS account that hosts Hyperglance by running: `aws configure`

	__Note:__ You will need an [AWS IAM access and secret key](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds).
	
	Example:
	```bash
	$ aws configure
	AWS Access Key ID [None]: ENTER_YOUR_ACCESS_KEY_HERE
	AWS Secret Access Key [None]: ENTER_YOUR_SECRET_KEY_HERE
	Default region name [None]: us-east-1
	Default output format [None]: json
	```
3. Clone our repo or  [download the zip](https://github.com/hyperglance/aws-rule-automations/archive/refs/heads/master.zip)
	```bash
	$ git clone https://github.com/hyperglance/aws-rule-automations.git
	```

4. Deploy the stack:
	> Terraform will prompt for the region you wish to deploy to and for final confirmation.
	```bash
	$ cd aws-rule-automations/deployment/terraform/automations
	$ terraform init
	$ terraform apply
	```

5. Once complete, the bucket name and lambda function ARN will be returned:
	```bash
	Apply complete! Resources: 8 added, 0 changed, 0 destroyed.

	Outputs:

	bucket_name = "hyperglance-automations-lucky-marmoset"
	lambda_arn = "arn:aws:lambda:us-east-1:0123456789:function:hyperglance-automations-lucky-marmoset"
	```
 
   *The lambda ARN is required to configure automations across accounts* 
	
	Copy these into the Hyperglance UI:  __Settings ➔ Automations ➔ S3 Bucket Name__
	or visit this URL: https://your-hyperglance-ip/#/admin/automations
	
	> __Note:__ Leave the 'Role ARN' field blank.
	This is only needed if you deploy the stack to a different AWS account from the Hyperglance Instance.

6. __That's it - Automations are now enabled!__
	* Within Hyperglance click on any rule or visit the Advanced Search page to start exploring automations features.
	* If you need automations to run on resources from _other_ AWS Accounts then continue on to follow our multi-account guide below.

## Cross-Account Deployment for Multiple Accounts

To grant the automations Lambda access to resources in __other__ AWS accounts you will need to create a special cross-account role in each of those accounts:

1. Edit `aws-rule-automations/deployment/terraform/xaccount_role/main.tf`
	* Set the `lambda_arn` to the arn of the lambda function which was given as an output in the main account configuration.
2. Connect to an AWS Account where you wish to deploy the Role:
	* Run: `aws configure`
	* You will need [AWS IAM access and secret keys](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds) for this account.

4. Deploy the Role:
	```bash
	$ cd aws-rule-automations/deployment/terraform/xaccount_role
	$ terraform init
	$ terraform apply
	```

## Keeping The Deployment Up-To-Date
__Note:__ When you first ran `terraform apply` Terraform created a tfstate file in the local directory to track the resources it created. In order to update the existing deployment you need that tfstate file to be in the `deployment/terraform/automations` directory.

To update your deployment you will need to:

1. Pull the latest updates from git (or [download the latest zip](https://github.com/hyperglance/aws-rule-automations/archive/refs/heads/master.zip) but make sure to copy over the same tfstate - see note above).
	```bash
	$ cd aws-rule-automations
	$ git pull
	```
2. If not still authenticated with AWS then re-run `aws configure`
3. Re-apply the terraform stack:
	```bash
	$ cd deployment/terraform/automations
	$ terraform apply
	```

Terraform will apply any updates to the cloud resources it already created.

It is a good idea to also [update the Hyperglance application](https://support.hyperglance.com/knowledge/upgrading-hyperglance-to-a-newer-version) at the same time.


## Customizing Automations
__Easily add your own automations or modify existing ones!__

Automations are written in Python3, each one is a self-contained Python (`.py`) file.
Find them here: https://github.com/hyperglance/aws-rule-automations/tree/master/lambda/automations

To add a new automation:
* Add a new .py file
* Implement the `hyperglance_automation()` function with logic for your automation.
* Implement the `info()` function to inform the Hyperglance UI about your automation:
	* Name,
	* Description,
	* Any UI inputs it needs from the user,
	* A list of compatible resource types.
* Re-deploy the terraform stack with `terraform apply`
* __Done__: Your new automation will be immediately available and ready to use in the Hyperglance UI.


## Contributions
Are welcome!
