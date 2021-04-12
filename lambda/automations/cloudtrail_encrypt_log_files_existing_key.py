"""
This automation encrypts log files in cloudtrail using an existing key

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

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

  client = boto_session.client('cloudtrail')

  cloudtrail_name = resource_id
  key_id = automation_params.get("Key ID")

  try:
    client.update_trail(
      Name=cloudtrail_name,
      KmsKeyId=key_id
    )

    automation_output = "Enabled encryption on Cloudtrail: {} using KMS Key: {}".format(cloudtrail_name, key_id)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output

def info() -> dict:

  INFO = {
    "displayName": "Encrypt Cloudtrail Logs - Existing Key",
    "description": "Encrypts Cloudtrail Logs, using an existing KMS Key",
    "resourceTypes": [
      "Cloudtrail"
    ],
    "params": [
      {
        "name": "Key ID",
        "type": "string",
        "default": " "
      }
    ]
  }

  return INFO