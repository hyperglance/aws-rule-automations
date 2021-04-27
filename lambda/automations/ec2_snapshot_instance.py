"""EC2 Snapshot Instance

This automation Snapshots an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import os

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to Snapshot and EC2 Instance

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

  client = boto_session.client('ec2')
  ec2_instance = resource['attributes']['Instance ID']
  vol_id = resource['attributes']['Volume ID']
    
  response = client.create_snapshot(
    Description="Snapshot created by Hyperglance",
    VolumeId=vol_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )
  
  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    automation_output = "An unexpected error occured, error message: {}".format(result)
  else:
    automation_output = "Snapshot Creation for Volume: {} started...".format(vol_id)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Snapshot Instance",
    "description": "Snapshots attached EBS Volumes",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO