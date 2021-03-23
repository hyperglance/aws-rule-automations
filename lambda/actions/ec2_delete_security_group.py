"""EC2 Delete Security Group

This action Deletes a Security Group, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os
from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Delte a Security Group

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

  client = boto_session.client('ec2')
  sg_id = resource_id

  try:
    response = client.delete_security_group(
      GroupId=sg_id,
      DryRun=action_params.get('DryRun').lower() in ['true', 'y', 'yes']
    )
    result = response['ResponseMetadat']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occurred, error message {}".format(result)
    else:
      action_output = "Security Group {} deleted.".format(sg_id)

  except ClientError as err:
    action_output = "An unexpected CLient Error Occured {}".format(err)

  return action_output


def info() -> dict:
  INFO = {
    "displayName": "Delete Security Group",
    "description": "Deletes a specified Security Group",
    "resourceTypes": [
      "Security Group"
    ],
    "params": [

    ]
  }

  return INFO