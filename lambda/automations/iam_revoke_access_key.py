"""
This automation Revokes a IAM User Access Key, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to revoke a User Access Key

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

  client = boto_session.client('iam')
  user_name = resource['attributes']['user name']

  automation_output = ''

  for rows, row in enumerate(table):
    try:
      client.update_access_key(
        UserName=user_name,
        AccessKeyId=row['Access Key Id'],
        Status='Inactive'
      )
      automation_output += "Access Key: {} for user: {} revoked".format(row['Access Key Id'], user_name)

    except ClientError as err:
      automation_output += "An unexpected client error occured, error: {}".format(err)

  return automation_output
  

def info() -> dict:
  INFO = {
    "displayName": "Revoke Access Key",
    "description": "Revokes IAM User Access Keys",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO