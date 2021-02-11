## ec2_delete_key_pair

## Deltes EC2 Keypair identified by Configured Hyperglance Rules
import boto3
from botocore.exceptions import ClientError

## Stop Workspace
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  keypair = entity['id']

  try:
    response = client.delete_key_pair(
      KeyName=keypair
    )

    action_output = "KeyPair {} was deleted successfully".format(keypair)

  except ClientError as err:
    action_output = "An unexpected error occured, error message: {}".format(str(err))

  return action_output