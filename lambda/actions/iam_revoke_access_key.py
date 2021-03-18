"""
This action Revokes a IAM User Access Key, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to revoke a User Access Key

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

  action_output = ''

  for rows, row in enumerate(table):
    try:
      client.update_access_key(
        UserName=user_name,
        AccessKeyId=row['Access Key Id'],
        Status='Inactive'
      )
      action_output += "Access Key: {} for user: {} revoked".format(row['Access Key Id'], user_name)

    except ClientError as err:
      action_output += "An unexpected client error occured, error: {}".format(err)

  return action_output
  

def info() -> str:
  INFO = {
    "displayName": "Revoke Access Key",
    "description": "Revokes IAM User Access Keys",
    "resourceTypes": [
      "IAM User",
      "IAM"
    ],
    "params": [

    ]
  }

  return INFO