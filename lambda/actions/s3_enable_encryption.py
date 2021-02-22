"""S3 Enable Encryption

This action Enables encryption on S3 Buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to add Encryption to an S3 Bucket

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

  client = boto_session.client('s3')
  bucket_name = resource_id

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
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "Bucket {} encryption enabled".format(bucket_name)
  
  except ClientError as err:
    action_output = "An unexpected Client Error occured, error message: {}".format(err)

  return action_output