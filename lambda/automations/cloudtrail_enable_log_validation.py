"""
This automation Enables cloudtrail log file validation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to enable cloudtrail log file validation

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

  client = boto_session.client('cloudtrail')
  cloudtrail_name = resource['attributes']['Cloudtrail ID']

  try:
    client.update_trail(
      Name=cloudtrail_name,
      EnableLogFileValidation=True
    )
    automation_output = "Cloud trail log file validation enabled on: {}".format(cloudtrail_name)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Enable Cloudtrail Validation",
    "description": "Enables Cloudtrail Log Validation",
    "resourceTypes": [
      "Cloudtrail"
    ],
    "params": [

    ]
  }

  return INFO