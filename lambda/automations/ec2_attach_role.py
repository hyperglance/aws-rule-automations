"""EC2 Attach Role

This automation attaches and IAM role to an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to attach an IAM policy to an EC2 Instance

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

  instance = resource['attributes']['Instance ID']
  role_arn = automation_params.get('Role')
  
  client.associate_iam_instance_profile(
    IamInstanceProfile={
      'Arn': role_arn,
      'Name': role_arn.split('/')[1]
    },
    InstanceId=instance
  )

def info() -> dict:
  INFO = {
    "displayName": "Attach IAM Role",
    "description": "Attaches and IAM role to an Instance",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [
      {
        "name": "Role",
        "type": "string",
        "default": " "
      }
    ],
    "permissions": [
      "ec2:AssociateIamInstanceProfile"
    ]
  }

  return INFO