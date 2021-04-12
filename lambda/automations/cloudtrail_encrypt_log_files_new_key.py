"""
This automation Creates a new key with appropriate policy to encrypte log files in cloudtrail

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import json

POLICY = {
    "Version": "2012-10-17",
    "Id": "Key policy created by Hyperglance automations",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::_TARGET_ACCOUNT_:user/_TARGET_USER_"
            },
            "automation": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow CloudTrail to encrypt logs",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "automation": "kms:GenerateDataKey*",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:_TARGET_ACCOUNT_:trail/*"
                }
            }
        },
        {
            "Sid": "Allow CloudTrail to describe key",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "automation": "kms:DescribeKey",
            "Resource": "*"
        },
        {
            "Sid": "Allow principals in the account to decrypt log files",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "automation": [
                "kms:Decrypt",
                "kms:ReEncryptFrom"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:CallerAccount": "_TARGET_ACCOUNT_"
                },
                "StringLike": {
                    "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:_TARGET_ACCOUNT_:trail/*"
                }
            }
        }
    ]
}


def create_policy(client, target_account: str) -> str:
  """ Attempts to Create a policy to enable Key Encryption

  Parameters
  ----------
  client: object
    The boto IAM client used to get user
  target_account : str
    Target Account for the Policy

  Returns
  -------
  string
    A string containing the status of the request

  """

  try:
    response = client.get_user()
    user_name = response['User']['UserName']

    kms_policy = json.dumps(POLICY)

    kms_policy = kms_policy.replace("_TARGET_ACCOUNT_", target_account)
    kms_policy = kms_policy.replace("_TARGET_USER_", user_name)

    automation_output = "Policy: {}".format(POLICY)

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def create_key(kms_client, iam_client, target_account: str, cloudTrail_name: str) -> str:
  """ Attempts to create a User Key

  Parameters
  ----------
  kms_client : object
    The boto kms client
  iam_client : onject
    The boto iam client
  target_account : str
    Target account for the KMS Key
  cloudtrail_name : str
    Name of target Cloudtrail logs

  Returns
  -------
  string
    A string containing the status of the request

  """

  try:
    kms_policy = create_policy(
      client=kms_client,
      target_account=target_account
    )

    response = kms_client.create_key(
      Policy=kms_policy,
      Description="Key for Cloudtrail: {}".format(cloudTrail_name)
    )

    created_key = response['KeyMetadata']['KeyId']

    ## Rotate the Key
    kms_client.enable_key_rotation(
      KeyId=created_key
    )

    automation_output = "{}".format(created_key)

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Enable Encryption on Cloudtrail

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  ## Setup required sessions
  cloudtrail_client = boto_session.client('cloudtrail')
  iam_client = boto_session.client('iam')
  kms_client = boto_session.client('kms')

  cloudtrail_name = resource_id
  target_account = table[0]['Account ID']

  try:
    key = create_key(
      kms_client=kms_client,
      iam_client=iam_client,
      target_account=target_account,
      cloudTrail_name=cloudtrail_name
    )

    ## Finally enable the encryption
    cloudtrail_client.update_trail(
      Name=cloudtrail_name,
      KmsKeyId=key,
      EnableLogFileValidation=True,
    )

    automation_output = "CloudTrail: {} encrypt log files using key: {}".format(cloudtrail_name.split('/')[-1], key)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Encrypt Cloudtrail Logs - New Key",
    "description": "Encrypts Cloudtrail Logs, using a new generated KMS Key",
    "resourceTypes": [
      "Cloudtrail"
    ],
    "params": [

    ]
  }

  return INFO