"""IAM Force User Password Change

This automation Disables a Users console access password, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to force a user password change

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client("iam")
  user_name = resource_id

  response = client.update_login_profile(
    UserName=user_name,
    PasswordResetRequired=True
  )

  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    automation_output = "An unexpected error occured, error message: {}".format(result)
  else:
    automation_output = "Password reset enabled for user: {}".format(user_name)
  
  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Force Password Change",
    "description": "Forces user to change their password on next login",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO