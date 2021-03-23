"""EC2 Delete Internet Gateway

This action Deletes and Internet Gateway, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Delete and Internet Gateway

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
  gateway_id = resource_id

  response = client.delete_internet_gateway(
    InternetGatewayId=gateway_id,
    DryRun=action_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(result)
  else:
    action_output = "Internet Geteway: {} deleted".format(gateway_id)

  return action_output


def info() -> dict:
  INFO = {
    "displayName": "Delete Internet Gateway",
    "description": "Deletes a specified Internet Gateway",
    "resourceTypes": [
      "Internet Gateway"
    ],
    "params": [

    ]
  }

  return INFO