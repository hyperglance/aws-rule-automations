"""S3 Enable Versioning

This automation Enables versioning on S3 Buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Enable versioning on an S3 Bucket

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

  client.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={
      'MFADelete': 'Disabled',
      'Status': 'Enabled'
    },
  )


def info() -> dict:
  INFO = {
    "displayName": "Enable S3 Versioning",
    "description": "Enables Object Versioning",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [
      "s3:PutBucketVersioning"
    ]
  }

  return INFO