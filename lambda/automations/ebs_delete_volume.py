"""EBS Delete Volumes

This automation Deltes an EBS Volume, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

## Delete EBS Snapshot
def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to Delete and EBS Volume

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
  ebs_volume = resource['attributes']['Volume ID']

  response = client.delete_volume(
    VolumeId=ebs_volume
  )

  ## Wait for the deletion to finish
  waiter = client.get_waiter('volume_deleted')

  waiter.wait(
    VolumeIds=[ebs_volume]
  )

  result = response['ResponseMetadata']['HTTPStatusCode']

  if result >= 400:
    automation_output = "An unexpected error occured, error message: {}".format(result)
  else:
    automation_output = "EBS Volume: {} deleted".format(ebs_volume)

  return automation_output


def info() -> dict:
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