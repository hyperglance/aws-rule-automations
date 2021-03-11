"""
This action Deletes a IAM User Access Key, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ]) -> str:
  """ Attempts to delete a User Access Key

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on
  table : list
    A list of additional resource values that may be required

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
      client.delete_access_key(
        UserName=user_name,
        AccessKeyId=row['Access Key Id']
      )
      action_output += "Access Key: {} for user: {} deleted".format(row['Access Key Id'], user_name)

    except ClientError as err:
      action_output += "An unexpected client error occured, error: {}".format(err)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Delete Access Keys",
    "description": "Deletes IAM Access Keys",
    "resourceTypes": [
      "IAM User",
      "IAM"
    ],
    "params": [

    ]
  }

  return INFO
