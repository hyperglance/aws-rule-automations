## ec2_delete_security_group

## Deletes Security Groups identified by configured Hyperglance Rules.
import os
import boto3
from botocore.exceptions import ClientError

## Enables S3 Encryption
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('ec2')
  sg_id = entity['id']

  try:
    response = client.delete_security_group(
      GroupId=sg_id,
      DryRun=os.environ['DryRun']
    )
    result = response['ResponseMetadat']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occurred, error message {}".format(str(result))
    else:
      action_output = "Security Group {} deleted.".format(sg_id)

  except ClientError as err:
    action_output = "An unexpected CLient Error Occured {}".format(err)

  return action_output