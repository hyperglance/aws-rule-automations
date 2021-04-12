"""EC2 Snapshot Instance

This automation Snapshots an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import os

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Snapshot and EC2 Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  ec2_instance = resource_id

  if len(table[0]['Volume ID']) == 0:
    automation_output = "No EBS Volumes, cannot snapshot {}.".format(ec2_instance)
    return automation_output
    
  response = client.create_snapshot(
    Description="Snapshot created by Hyperglance",
    VolumeId=table[0]['Volume ID'],
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )
  
  ## Wait for Snapshot
  waiter = client.get_waiter('snapshot_completed')

  waiter.wait(
    Filters=[
      {
        'volume-id': table[0]['Volume ID']
      }
    ]
  )

  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    automation_output = "An unexpected error occured, error message: {}".format(result)
  else:
    automation_output = "Snapshot Creation for Volume: {} started...".format(table[0]['Volume ID'])

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Snapshot Instance",
    "description": "Snapshots attached EBS Volumes",
    "resourceTypes": [
      "EBS Volume",
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO