"""IAM Disable User Console Password

This action Disables a Users console access password, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to deletes a users console access password

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

  client = boto_session.client('iam')
  user_name = resource_id

  try:
    user_profile = client.LoginProfile(user_name)
    user_profile.delete()
    action_output = "User {} console access password was deleted".format(user_name)

  except ClientError as err:
    action_output = "An unexpected error occured, error message: {}".format(err)
  
  return action_output


def info() -> dict:
  INFO = {
    "displayName": "Disable Console Access",
    "description": "Disables a users console access, but leaves programmatic access intact",
    "resourceTypes": [
      "IAM",
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO