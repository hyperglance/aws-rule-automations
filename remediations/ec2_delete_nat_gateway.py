## ec2_delete_nat_gateway

## Deletes a NAT Gateway identified by configured Hyperglance Rules
import os
from boto3 import session, ec2

## Delete NAT Gateway
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  gateway_id = entity['id']

  response = client.delete_nat_gateway(
    NatGatewayId=gateway_id,
    DryRun=os.environ['DryRun']
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(str(result))
  else:
    action_output = "NAT Geteway: {} deleted".format(gateway_id)

  return action_output