"""S3 Block Public Access

This automation Blocks Public Access to S3 buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

AWS Definition of Public:
https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Block all Puiblic access to an S3 Bucket

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

  client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
      'BlockPublicAcls': True,
      'IgnorePublicAcls': True,
      'BlockPublicPolicy': True,
      'RestrictPublicBuckets': True
    }
  )


def info() -> dict:
  INFO = {
    "displayName": "Block S3 Public Access",
    "description": "Blocks all public access to an S3 Bucket",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ],
    "permissions": [
      "s3:PutBucketPublicAccessBlock"
    ]
  }

  return INFO