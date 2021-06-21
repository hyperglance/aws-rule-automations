"""S3 Enable Encryption

This automation Enables encryption on S3 Buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to add Encryption to an S3 Bucket

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('s3')
  bucket_name = resource['id']

  client.put_bucket_encryption(
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