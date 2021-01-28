## ec2_terminate_instance

## Terminates and optionally Snapshots instances identified by configured Hyperglance Rules.
import os
import boto3
import remediations.ec2_snapshot_instance


## Stop EC2 Instance
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  ec2_instance = entity['id']

  if os.environ['SnapShotBeforeTerminate']:
    ec2_snapshot_instance = ec2_snapshot_instance()
    response = ec2_snapshot_instance(
      boto_session, 
      rule, 
      entity, 
      params
      )

  if response['ResponseMetadata']['HTTPStatusCOde'] >= 400:
    action_output = "Something went wrong with the snapshot for instance {}, abandoning termination".format(ec2_instance)
    return action_output
  else:
    response = client.terminate_instances(
      InstanceIds=[ec2_instance], 
      DryRun=os.environ['DryRun']
      )

    result = response['ResponseMetadata']['HTTPStatusCode']
    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(str(result))
    else:
      action_output = "Instance {} stopped".format(ec2_instance)

    return action_output