"""
This action deactivates unused access keys, and sets it to latest version, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os
from botocore.exceptions import ClientError
from datetime import datetime


def days_last_used(client, access_key) -> int:
  """ Calculates when a key was last used

  Parameters
  ----------
  client : object
    The boto client used to make the call
  access_key : str
    Target access key to check

  Returns
  -------
  int
    The number of days since the key was last used

  """

  ## Get current date and time
  current_date_time = datetime.now()
  ## Access Key ID
  access_key_id = access_key['AccessKeyId']
  ## Get the last used details
  key_last_used = client.get_access_key_last_used(
    AccessKeyId=access_key_id
  ) ['AccessKeyLastUsed']

  ## Check if key has ever been used, else use creation time
  if 'LastUsedDate' in key_last_used:
    return (current_date_time - key_last_used['LastUsedDate'].replace(tzinfo=None)).days
  else:
    return (current_date_time - access_key['CreateDate'].replace(tzinfo=None)).days


def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ]) -> str:
  """ Attempts to delete default policy and set to the LATEST

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
  iam_username = resource_id

  max_days_unused = os.getenv("KeysMaxDaysUnused")

  try:
    ## Get all the access keys for the user
    iam_user_access_keys = client.list_access_keys(
      UserName=iam_username,
      MaxItems=os.getenv("MaxKeyItems")
    )

    for key in iam_user_access_keys:
      ## Get access key ID
      access_key_id = key['AccessKeyId']
      ## Get number of days since last use
      days_since_last_use = days_last_used(client=client, access_key_id=access_key_id)

      if days_since_last_use > max_days_unused:
        ## Deactivate the Key
        client.update_access_key(
          UserName=iam_username,
          AccessKeyId=access_key_id,
          Status='Inactive'
        )
        action_output = "IAM User: {} access key id: {} has been deactivated"

  except ClientError as err:
    action_output = "An unexpected client error has occured, error: {}".format(err)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Deactivate Keys",
    "description": "Deactivates Unused Access Keys",
    "resourceTypes": [
      "IAM User",
      "IAM"
    ],
    "params": [
      {
        "name": "MaxKeyItems",
        "type": "number",
        "default": "10",
        "min": "5",
        "max": "200"
      }
    ]
  }

  return INFO