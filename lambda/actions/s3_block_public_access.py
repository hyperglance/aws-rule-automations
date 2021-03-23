"""S3 Block Public Access

This action Blocks Public Access to S3 buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

AWS Definition of Public:
https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Block all Puiblic access to an S3 Bucket

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

  client = boto_session.client('s3')
  bucket_name = resource_id

  try:
    response = client.put_public_access_block(
      Bucket=bucket_name,
      PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
      }
    )
    action_output = "Bucket {} public access blocked".format(bucket_name)

  except ClientError as err:
    action_output = "An unexpected error occured, error message: {}".format(err)
  
  return action_output


def info() -> dict:
  INFO = {
    "displayName": "Block S3 Public Access",
    "description": "Blocks all public access to S3 Bucket",
    "resourceTypes": [
      "S3",
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO