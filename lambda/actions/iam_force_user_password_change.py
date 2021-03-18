"""IAM Force User Password Change

This action Disables a Users console access password, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to force a user password change

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

  client = boto_session.client("iam")
  user_name = resource_id

  try:
    response = client.update_login_profile(
      UserName=user_name,
      PasswordResetRequired=True
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "Password reset enabled for user: {}".format(user_name)
  
  return action_output


def info() -> str:
  INFO = {
    "displayName": "Force Password Change",
    "description": "Forces user to change their password on next login",
    "resourceTypes": [
      "IAM",
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO