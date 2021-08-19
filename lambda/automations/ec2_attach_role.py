"""EC2 Attach Role

This automation attaches and IAM role to an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import logging
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



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

  ec2 = boto_session.client('ec2')
  iam = boto_session.client('iam')
  ec2_instance = resource['attributes']['Instance ID']
  role_name = automation_params.get('Role')
  instance_profile_name = role_name + str(random.randint(10000, 99999))

  instance_profile = iam.create_instance_profile(
    InstanceProfileName=instance_profile_name
  )


  instance_profile_arn = instance_profile['InstanceProfile']['Arn']


  iam.add_role_to_instance_profile(
    InstanceProfileName=instance_profile_name,
    RoleName=role_name
  )

  ec2.associate_iam_instance_profile(
    IamInstanceProfile={
      'Arn': instance_profile_arn,
      'Name': instance_profile_name
    },
    InstanceId=ec2_instance
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
      "ec2:AssociateIamInstanceProfile",
      "iam:GetRole",
      "iam:CreateInstanceProfile",
      "iam:PassRole",
      "iam:AddRoleToInstanceProfile"
    ]
  }

  return INFO