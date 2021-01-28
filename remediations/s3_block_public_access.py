## s3_block_public_access

## Blocks Public Access to S3 resources Identified by Configured Hyperglance Rule
import boto3
from botocore.exceptions import ClientError

## AWS Definition of Public
## https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status

## Block S3 Public Access
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('s3')
  bucket_name = entity['id']

  try:
    response = client.put_public_access_block(
      Bucket=bucket_name,
      PublicAcessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
      }
    )
    action_output = "Bucket {} public access blocked".format(bucket_name)

  except ClientError as err:
    action_output = "An unexpected error occured, error message: {}".format(str(response))
  
  return action_output
