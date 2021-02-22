"""
This action Enables cloudtrail log file validation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to enable cloudtrail log file validation

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

  client = boto_session.client('cloudtrail')
  cloudtrail_name = resource_id

  try:
    client.update_trail(
      Name=cloudtrail_name,
      EnableLogFileValidation=True
    )
    action_output = "Cloud trail log file validation enabled on: {}".format(cloudtrail_name)

  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)

  return action_output