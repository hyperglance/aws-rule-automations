## ec2_snapshot_instance

## Snapshots instances identified by configured Hyperglance Rules.
import os
import boto3

## Stop EC2 Instance
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  ec2_instance = entity['id']

  if len(entity['volumes']) == 0:
    action_output = "No EBS Volumes, cannot snapshot {}.".format(ec2_instance)
    return action_output

  for vol in entity['volumes']:
    vol_id = vol['volumeId']
    
    response = client.create_snapshot(
      Description="Snapshot created by Hyperglance rule {}".format(rule['name']),
      VolumeId=vol_id,
      DryRun=os.environ['DryRun']
    )
  ## TODO: Add waiter
  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(str(result))
  else:
    action_output = "Snapshot Creation for Volume: {} started...".format(vol_id)

  return action_output