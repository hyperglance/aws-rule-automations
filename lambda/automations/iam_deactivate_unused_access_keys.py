"""
This automation deactivates unused access keys, and sets it to latest version, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

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
  access_key_id = access_key.get('Access Key Id')
  ## Get the last used details
  key_last_used = client.get_access_key_last_used(
    AccessKeyId=access_key_id
  ) ['AccessKeyLastUsed']

  ## Check if key has ever been used, else use creation time
  if 'LastUsedDate' in key_last_used:
    return (current_date_time - key_last_used['LastUsedDate'].replace(tzinfo=None)).days
  else:
    return (current_date_time - access_key['CreateDate'].replace(tzinfo=None)).days


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to delete default policy and set to the LATEST

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
  iam_username = resource['attributes']['User Name']

  max_days_unused = automation_params.get('MaxDaysUsed')

  try:
    ## Get all the access keys for the user
    iam_user_access_keys = client.list_access_keys(
      UserName=iam_username,
      MaxItems=int(automation_params.get('MaxKeyItems'))
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
        automation_output = "IAM User: {} access key id: {} has been deactivated"

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Deactivate Keys",
    "description": "Deactivates Unused Access Keys",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [
      {
        "name": "MaxKeyItems",
        "type": "number",
        "default": "10",
        "min": "5",
        "max": "200"
      },
      {
        "name": "MaxDaysUsed",
        "type": "Number",
        "default": "90"
      }
    ]
  }

  return INFO