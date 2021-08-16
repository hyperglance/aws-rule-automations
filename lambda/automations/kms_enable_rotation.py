"""
This automation Enables KMS Key Rotation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to enable KMS Key Rotation

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('kms')
  kms_key = automation_params.get('KMS Key')

  client.enable_key_rotation(
    KeyId=kms_key
  )

  
def info() -> dict:
  INFO = {
    "displayName": "Enable KMS Rotation",
    "description": "Enables rotations of KMS Keys",
    "resourceTypes": [
      "IAM"
    ],
    "params": [
      {
        "name": "KMS Key",
        "type": "string",
        "default": ""
      }
    ],
    "permissions": [
      "kms:EnableKeyRotation"
    ]
  }

  return INFO