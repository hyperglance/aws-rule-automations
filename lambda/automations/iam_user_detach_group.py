"""Detaches an IAM User for a Group

This automation detaches a user from a user group, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to detach a user from a group

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
  group_id = automation_params.get('Group')

  try:
    client.remove_user_from_group(
      GroupName=group_id,
      UserName=user_name
    )
    automation_output = "Removed user: {} from group: {} successfully".format(user_name, group_id)

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Detach User from Group",
    "description": "Detaches a user from a specifid User Group",
    "resourceTypes": [
      "IAM"
    ],
    "params": [
      {
        "name": "Group",
        "type": "string",
        "default": ""
      }
    ]
  }

  return INFO