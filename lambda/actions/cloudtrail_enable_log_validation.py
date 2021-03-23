"""
This action Enables cloudtrail log file validation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to enable cloudtrail log file validation

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

  client = boto_session.client('cloudtrail')
  cloudtrail_name = resource_id

  try:
    client.update_trail(
      Name=cloudtrail_name,
      EnableLogFileValidation=True
    )
    action_output = "Cloud trail log file validation enabled on: {}".format(cloudtrail_name)

  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)

  return action_output


def info() -> dict:
  INFO = {
    "displayName": "Enable Cloudtrail Validation",
    "description": "Enables Cloudtrail Log Validation",
    "resourceTypes": [
      "Cloudtrail"
    ],
    "params": [

    ]
  }

  return INFO