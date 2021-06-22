"""EC2 Terminate Instance

This automation Terminates an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import automations.ec2_snapshot_instance


## Stop EC2 Instance
def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Terminate an EC2 Instance

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

  if automation_params.get('SnapShotBeforeTerminate').lower() in ['true', 'y', 'yes']:
    automations.ec2_snapshot_instance.hyperglance_automation(
      boto_session, 
      resource,
      automation_params
    )

  client.terminate_instances(
    InstanceIds=[ec2_instance], 
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )

  
def info() -> dict:
  INFO = {
    "displayName": "Terminate Instance",
    "description": "Terminates EC2 Instance",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "bool",
        "default": "True"
      },
      {
        "name": "SnapShotBeforeTerminate",
        "type": "bool",
        "default": "True"
      }
    ]
  }

  return INFO