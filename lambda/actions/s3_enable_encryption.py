## s3_enable_encryption

## Enables encryption on S3 Resources identified by configured Hyperglance Rules.
import boto3
from botocore.exceptions import ClientError

## Enables S3 Encryption
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('s3')
  bucket_name = entity['id']

  try:
    response = client.put_bucket_encryption(
      Bucket=bucket_name,
      ServerSideEncryptionConfiguration={
        'Rules': [
          {
            'ApplyServerSideEncryptionByDefault': {
              'SSEAlgorithm': 'AES256'
            },
          }
        ],
      }
    )
    result = response['ResponseMetadata']['HTTPStatusCode']
    
    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(str(result))
    else:
      action_output = "Bucket {} encryption enabled".format(bucket_name)
  
  except ClientError as err:
    action_output = "An unexpected Client Error occured, error message: {}".format(err)

  return action_output