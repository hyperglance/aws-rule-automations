"""EBS Delete Volumes

This automation Deltes an EBS Volume, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

## Delete EBS Snapshot
def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete and EBS Volume

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """
  client = boto_session.client('ec2')
  ebs_volume = resource['attributes']['Volume ID']

  client.delete_volume(
    VolumeId=ebs_volume
  )

  ## Wait for the deletion to finish
  client.get_waiter('volume_deleted').wait(
    VolumeIds=[ebs_volume]
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete EBS Volume",
    "description": "Deletes a specified EBS Volume",
    "resourceTypes": [
      "EBS Volume"
    ],
    "params": [

    ],
    "permissions": [
      "ec2:DeleteVolume"
    ]
  }

  return INFO