## ebs_delete_snapshot

## Deletes Unused Snapshots identified bt configured Hyperglance Rules
import os
from boto3 import ec2, session

## Delete EBS Snapshot
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  ebs_volume = entity['id']

  response = client.delete_volume(
    VolumeId=ebs_volume
  )

  ## Wait for the deletion to finish
  waiter = client.get_water('volume_deleted')

  waiter.wait(
    VolumeId=ebs_volume
  )

  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(str(result))
  else:
    action_output = "EBS Volume: {} deleted".format(ebs_volume)

  return action_output