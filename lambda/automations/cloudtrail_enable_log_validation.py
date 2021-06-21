"""
This automation Enables cloudtrail log file validation, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to enable cloudtrail log file validation

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('cloudtrail')
  cloudtrail_name = resource['attributes']['Cloudtrail ID']

  client.update_trail(
    Name=cloudtrail_name,
    EnableLogFileValidation=True
  )

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