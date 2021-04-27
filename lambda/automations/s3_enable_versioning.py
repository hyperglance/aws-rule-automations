"""S3 Enable Versioning

This automation Enables versioning on S3 Buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to Enable versioning on an S3 Bucket

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
    response = client.put_bucket_versioning(
      Bucket=bucket_name,
      VersioningConfiguration={
        'MFADelete': 'Disabled',
        'Status': 'Enabled'
      },
    )
    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      automation_output = "An unexpected error occured, error message: {}".format(result)
    else:
      automation_output = "Bucket {} enabled for versioning".format(bucket_name)
    
  except ClientError as err:
    automation_output = "An unexpected Client error Occured, error message: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Enable S3 Versioning",
    "description": "Enables Object Versioning",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO