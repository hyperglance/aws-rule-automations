"""EC2 Delete NAT Gateway

This action Deletes a NAT Gateway, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os
import boto3

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to Delete a NAT Gateway

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  gateway_id = resource_id

  response = client.delete_nat_gateway(
    NatGatewayId=gateway_id,
    DryRun=os.getenv("DryRun", 'False').lower() in ['true', '1', 'y', 'yes']
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(result)
  else:
    action_output = "NAT Geteway: {} deleted".format(gateway_id)

  return action_output