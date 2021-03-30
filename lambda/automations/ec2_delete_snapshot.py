"""EC2 Delete Snapshot

This automation Deletes and EC2 Snapshot, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import os

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Delete and EC2 Snapshot

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
  snapshot_id = resource_id

  response = client.delete_snapshot(
    SnapshotId=snapshot_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    automation_output = "An unexpected error occured, error message:".format(result)
  else:
    automation_output = "Snapshot: {} deleted".format(snapshot_id)
  
  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Delete EBS Snapshot",
    "description": "Deletes a specified EBS Snapshot",
    "resourceTypes": [
      "EBS Snapshot"
    ],
    "params": [

    ]
  }

  return INFO