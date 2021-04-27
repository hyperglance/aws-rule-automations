"""IAM Disable User Console Password

This automation Disables a Users console access password, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to deletes a users console access password

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
  user_name = resource['attributes']['User Name']

  try:
    user_profile = client.LoginProfile(user_name)
    user_profile.delete()
    automation_output = "User {} console access password was deleted".format(user_name)

  except ClientError as err:
    automation_output = "An unexpected error occured, error message: {}".format(err)
  
  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Disable Console Access",
    "description": "Disables a users console access, but leaves programmatic access intact",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO