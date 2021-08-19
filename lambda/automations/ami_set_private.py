"""AMI Set To Private

This automation Sets and AMI to Private for AMIs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to set an AMI to Private

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

  ami_id = resource['attributes']['AMI ID']
  owner_id = resource['attributes']['Owner ID']

  client.modify_image_attribute(
    ImageId=ami_id,
    LaunchPermission={
      'Remove': [
        {
          "Group": 'all',
          "UserId": owner_id
        },
      ]
    }
  )

def info() -> dict:
  INFO = {
    "displayName": "Set AMI to Private",
    "description": "Sets and AMI to Private if it is currently Public",
    "resourceTypes": [
      "AMI"
    ],
    "params": [

    ],
    "permissions": [
      "ec2:ModifyImageAttribute"
    ]
  }

  return INFO