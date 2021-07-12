"""EC2 Delete Key Pair

This automation Deletes a Key Pair, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

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

  client = boto_session.client('ec2')
  keypair = automation_params.get('Key Name')

  client.delete_key_pair(
    KeyName=keypair
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete EC2 Key Pair",
    "description": "Deletes a specified EC2 Key Pair",
    "resourceTypes": [
      "Region"
    ],
    "params": [
      {
        "name": "Key Name",
        "type": "string"
      }
    ]
  }

  return INFO