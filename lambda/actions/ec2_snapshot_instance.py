"""EC2 Snapshot Instance

This action Snapshots an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ], action_params = '') -> str:
  """ Attempts to Snapshot and EC2 Instance

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
  ec2_instance = resource_id

  if len(table[0]['volumes']) == 0:
    action_output = "No EBS Volumes, cannot snapshot {}.".format(ec2_instance)
    return action_output

  for vol in table[0]['volumes']:
    vol_id = vol['volumeId']
    
    response = client.create_snapshot(
      Description="Snapshot created by Hyperglance rule {}".format(rule),
      VolumeId=vol_id,
      DryRun=os.getenv("DryRun", 'False').lower() in ['true', '1', 'y', 'yes']
    )
  ## TODO: Add waiter
  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(result)
  else:
    action_output = "Snapshot Creation for Volume: {} started...".format(vol_id)

  return action_output


def info() -> str:
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