"""EC2 Detach Role

This automation removes the contents of an s3 bucket, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to clear an EC2 Instance

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
  response = client.list_objects(Bucket=bucket_name)


def info() -> dict:
  INFO = {
    "displayName": "Clear an S3 Bucket",
    "description": "Removes the contents of an S3 bucket",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ],
    "permissions": [
    ]
  }

  return INFO