"""IAM Force User Password Change

This automation Disables a Users console access password, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to force a user password change

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client("iam")
  user_name = resource['attributes']['User Name']

  client.update_login_profile(
    UserName=user_name,
    PasswordResetRequired=True
  )


def info() -> dict:
  INFO = {
    "displayName": "Force Password Change",
    "description": "Forces an IAM User to change their password on next login",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ],
    "permissions": [
      "iam:UpdateLoginProfile"
    ]
  }

  return INFO