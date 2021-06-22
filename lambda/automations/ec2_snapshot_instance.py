"""EC2 Snapshot Instance

This automation Snapshots an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Snapshot and EC2 Instance

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
  ec2_instance = resource['attributes']['Instance ID']
    
  client.create_snapshots(
    Description=f'Snapshot of {ec2_instance} created by Hyperglance',
    InstanceSpecification={
      'InstanceId': ec2_instance,
      'ExcludeBootVolume': False
    },
    CopyTagsFromSource='volume',
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Snapshot Instance",
    "description": "Snapshots attached EBS Volumes",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO