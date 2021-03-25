"""
This automation Enables KMS Key Rotation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to enable KMS Key Rotation

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

  client = boto_session.client('kms')
  kms_key = resource_id

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