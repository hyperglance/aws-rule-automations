"""
This action Enables KMS Key Rotation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to enable KMS Key Rotation

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

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
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "Key: {} rotation enabled".format(kms_key)

    return action_output

  
def info() -> str:
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