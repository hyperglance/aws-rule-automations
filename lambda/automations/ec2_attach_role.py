"""EC2 Attach Role

This automation attaches and IAM role to an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to attach an IAM policy to an EC2 Instance

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

  instance = resource['attributes']['Instance ID']
  role_arn = automation_params.get('Role')
  
  try:
    response = client.associate_iam_instance_profile(
      IamInstanceProfile={
        'Arn': role_arn,
        'Name': role_arn.split('/')[1]
      },
      InstanceId=instance
    )

    result = response['ResponseMetadata']['HTTPStatusCode']
    if result >= 400:
      automation_output = "An unexpected error occured, error: {}".format(result)
    else:
      automation_output = "Role: {} attached to instance: {} successfully".format(role_arn, instance)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output

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
    ]
  }

  return INFO