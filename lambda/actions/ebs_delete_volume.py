"""EBS Delete Volumes

This action Deltes an EBS Volume, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

## Delete EBS Snapshot
def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Delete and EBS Volume

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

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


def info() -> str:
  INFO = {
    "displayName": "Delete EBS Volume",
    "description": "Deletes a specified EBS Volume",
    "resourceTypes": [
      "EBS Volume"
    ],
    "params": [

    ]
  }

  return INFO