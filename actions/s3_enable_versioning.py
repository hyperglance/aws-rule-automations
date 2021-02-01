## s3_enable_versioning

## Enables versioning on S3 Resources identified by configured Hyperglance Rules.
import boto3
from botocore.exceptions import ClientError

## Enables S3 Encryption
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('s3')
  bucket_name = entity['id']

  try:
    response = client.put_bucket_versioning(
      Bucket=bucket_name,
      VersioningConfiguration={
        'MFADelete': 'Disabled',
        'Status': 'Enabled'
      },
    )
    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(str(result))
    else:
      action_output = "Bucket {} enabled for versioning".format(bucket_name)
    
  except ClientError as err:
    action_output = "An unexpected Client error Occured, error message: {}".format(err)

  return action_output