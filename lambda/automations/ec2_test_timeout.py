"""EC2 Delete Key Pair

This automation Deletes a Key Pair, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from time import sleep


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete a Key Pair

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  sleep(60)


def info() -> dict:
  INFO = {
    "displayName": "Zzzzzz",
    "description": "Does nothing for a minute",
    "resourceTypes": [
      "EC2"
    ],
    "params": [

    ],
    "permissions": [
    ]
  }

  return INFO