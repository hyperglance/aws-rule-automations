"""EBS Delete Volumes

This action Deltes an EBS Volume, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import boto3

## Delete EBS Snapshot
def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to Delete and EBS Volume

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on

  Returns
  -------
  string
    A string containing the status of the request

  """
  client = boto_session.client('ec2')
  ebs_volume = resource_id

  response = client.delete_volume(
    VolumeId=ebs_volume
  )

  ## Wait for the deletion to finish
  waiter = client.get_waiter('volume_deleted')

  waiter.wait(
    VolumeId=ebs_volume
  )

  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(result)
  else:
    action_output = "EBS Volume: {} deleted".format(ebs_volume)

  return action_output