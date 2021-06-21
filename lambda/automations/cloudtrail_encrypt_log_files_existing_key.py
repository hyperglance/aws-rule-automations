"""
This automation encrypts log files in cloudtrail using an existing key

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Enable Encryption on Cloudtrail

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('cloudtrail')

  cloudtrail_name = resource['attributes']['Cloudtrail ID']
  key_id = automation_params.get("Key ID")

  client.update_trail(
    Name=cloudtrail_name,
    KmsKeyId=key_id
  )

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