"""EBS Delete Volumes

This automation Deltes an EBS Volume, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
  ec2_client = boto_session.client('ec2')
  ec2_resource = boto_session.resource('ec2')
  ebs_volume = resource['attributes']['Volume ID']
  volume = ec2_resource.Volume(ebs_volume)
  detachment_waiter = ec2_client.get_waiter('volume_available')
  instance_waiter = ec2_client.get_waiter('instance_stopped')


  for instance in volume.attachments:


    response = ec2_client.stop_instances(
      InstanceIds=[
        instance['InstanceId']
      ],
      Force=True
    )


    instance_waiter.wait(
      InstanceIds=[
        instance['InstanceId']
      ]
    )

    response = volume.detach_from_instance(
      Device=instance['Device'],
      Force=True,
      VolumeId=instance['VolumeId'],
      InstanceId=instance['InstanceId']
    )

    detachment_waiter.wait(
      VolumeIds=[instance['VolumeId']])




  ec2_client.delete_volume(
    VolumeId=ebs_volume
  )

  ## Wait for the deletion to finish
  ec2_client.get_waiter('volume_deleted').wait(
    VolumeIds=[ebs_volume]
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete EBS Volume",
    "description": "Deletes a specified EBS Volume - Must not be attached to a spot request instance",
    "resourceTypes": [
      "EBS Volume"
    ],
    "params": [

    ],
    "permissions": [
      "ec2:DeleteVolume",
      "ec2:DescribeVolumes",
      "ec2:DetachVolume",
      "ec2:StopInstances",
      "ec2:DescribeInstances"
    ]
  }

  return INFO