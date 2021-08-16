"""EC2 Delete Security Group

This automation Deletes a Security Group, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delte a Security Group

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
  sg_id = resource['attributes']['Group ID']

  client.delete_security_group(
    GroupId=sg_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete Security Group",
    "description": "Deletes a specified Security Group",
    "resourceTypes": [
      "Security Group"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "boolean",
        "default": "true"
      }
    ],
    "permissions": [
      "ec2:DeleteSecurityGroup"
    ]
  }

  return INFO