## ec2_stop_instance

## Stops instances identified by configured Hyperglance Rules.
import os
import boto3


## Stop EC2 Instance
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  ec2_instance = entity['id']

  response = client.stop_instances(
    InstanceIds=[ec2_instance], 
    DryRun=os.environ['DryRun']
    )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(str(result))
  else:
    action_output = "Instance {} stopped".format(ec2_instance)

  return action_output