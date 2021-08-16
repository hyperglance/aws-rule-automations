"""Detaches an IAM User for a Group

This automation detaches a user from a user group, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to detach a user from a group

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('iam')

  user_name = resource['attributes']['User Name']
  group_id = automation_params.get('Group')

  client.remove_user_from_group(
    GroupName=group_id,
    UserName=user_name
  )


def info() -> dict:
  INFO = {
    "displayName": "Detach User from Group",
    "description": "Detaches a user from a specified User Group",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [
      {
        "name": "Group",
        "type": "string",
        "default": ""
      }
    ],
    "permissions": [
      "iam:RemoveUserFromGroup"
    ]
  }

  return INFO