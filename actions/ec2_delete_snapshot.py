## ec2_delete_snapshot

## Deletes snapshots identified by configured Hyperglance Rules.
import os
import boto3

## Stop EC2 Instance
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session('ec2')
  snapshot_id = entity['id']

  response = client.delete_snapshot(
    SnapshotId=snapshot_id,
    DryRun=os.environ['DryRun']
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message:".format(str(result))
  else:
    action_output = "Snapshot: {} deleted".format(snapshot_id)
  
  return action_output