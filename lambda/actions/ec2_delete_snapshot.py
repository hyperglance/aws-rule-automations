"""EC2 Delete Snapshot

This action Deletes and EC2 Snapshot, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ], action_params = '') -> str:
  """ Attempts to Delete and EC2 Snapshot

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on
  table : list
    A list of additional resource values that may be required

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  snapshot_id = resource_id

  response = client.delete_snapshot(
    SnapshotId=snapshot_id,
    DryRun=os.getenv("DryRun", 'False').lower() in ['true', '1', 'y', 'yes']
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message:".format(result)
  else:
    action_output = "Snapshot: {} deleted".format(snapshot_id)
  
  return action_output


def info() -> str:
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