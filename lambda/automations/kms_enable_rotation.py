"""
This automation Enables KMS Key Rotation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to enable KMS Key Rotation

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('kms')
  kms_key = resource['attrinutes']['KMS Key']

  try:
    response = client.enable_key_rotation(
      KeyId=kms_key
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      automation_output = "An unexpected error occured, error message: {}".format(result)
    else:
      automation_output = "Key: {} rotation enabled".format(kms_key)

    return automation_output

  
def info() -> dict:
  INFO = {
    "displayName": "Enable KMS Rotation",
    "description": "Enables rotations of KMS Keys",
    "resourceTypes": [
      "IAM"
    ],
    "params": [

    ]
  }

  return INFO