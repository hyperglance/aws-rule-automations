"""IAM Disable User Console Password

This action Disables a Users console access password, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import boto3
from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to deletes a users console access password

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on

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