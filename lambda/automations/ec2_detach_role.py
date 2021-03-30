"""EC2 Detach Role

This automation Detaches an Instance role, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Detach a role from an EC2 Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')
  role_name = resource_id

  try:
    response = client.list_instance_profiles_for_role(RoleName=role_name)['InstanceProfiles']
    if len(response) == 0:
      automation_output = "Role: {} is not attached to instance".format(role_name)
      return automation_output
    else:
      client.remove_role_from_instance_profile(
        InstanceProfileName=response[0]['InstanceProfileName'],
        RoleName=role_name
      )
      automation_output = "Successfully detached role: {} from instance".format(role_name)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)  
    
  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Detach IAM Role",
    "description": "Detaches a specified role from an EC2 Instance",
    "resourceTypes": [
      "EC2 Instance",
      "IAM"
    ],
    "params": [

    ]
  }

  return INFO