"""EC2 Detach Role

This automation Detaches an Instance role, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Detach a role from an EC2 Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('iam')
  role_name = automation_params.get('Role')
  ec2_instance = resource['attributes']['Instance ID']

  response = client.list_instance_profiles_for_role(RoleName=role_name)['InstanceProfiles']
  if len(response) == 0:
    automation_output = "Role: {} is not attached to instance".format(role_name)
    return automation_output
  else:
    client.remove_role_from_instance_profile(
      InstanceProfileName=response[0]['InstanceProfileName'],
      RoleName=role_name
    )


def info() -> dict:
  INFO = {
    "displayName": "Detach IAM Role",
    "description": "Detaches a specified role from an EC2 Instance",
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