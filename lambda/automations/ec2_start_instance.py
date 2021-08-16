"""EC2 Start Instance

This automation Starts an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Start an EC2 Instance

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
  ec2_instance = resource['attributes']['Instance ID']

  client.start_instances(
    InstanceIds=[ec2_instance],
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Start Instance",
    "description": "Immediately Starts an EC2 Instance",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "boolean",
        "default": "True"
      }
    ]
  }

  return INFO