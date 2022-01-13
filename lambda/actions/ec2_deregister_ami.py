"""EC2 Deregister Image

This automation de-registers an AMI image.

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Deregister an EC2 AMI Image

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
  ami_id = resource['id']

  client.deregister_image(
    ImageId=ami_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Deregister Image",
    "description": "Deregisters an AMI. (The EBS Snapshots are not removed by this action)",
    "resourceTypes": [
      "AMI"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "boolean",
        "default": "true"
      }
    ],
    "permissions": [
      "ec2:DeregisterImage"
    ]
  }

  return INFO