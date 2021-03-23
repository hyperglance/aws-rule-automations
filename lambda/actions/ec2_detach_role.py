"""EC2 Detach Role

This action Detaches an Instance role, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Detach a role from an EC2 Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

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
      action_output = "Role: {} is not attached to instance".format(role_name)
      return action_output
    else:
      client.remove_role_from_instance_profile(
        InstanceProfileName=response[0]['InstanceProfileName'],
        RoleName=role_name
      )
      action_output = "Successfully detached role: {} from instance".format(role_name)

  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)  
    
  return action_output


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