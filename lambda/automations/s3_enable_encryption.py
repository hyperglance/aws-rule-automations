"""S3 Enable Encryption

This automation Enables encryption on S3 Buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to add Encryption to an S3 Bucket

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('s3')
  bucket_name = resource['id']
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
      automation_output = "An unexpected error occured, error message: {}".format(result)
    else:
      automation_output = "Bucket {} encryption enabled".format(bucket_name)
  
  except ClientError as err:
    automation_output = "An unexpected Client Error occured, error message: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Enable S3 Encryption",
    "description": "Enables AES265 Encryption on S3 Bucket Objects",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO