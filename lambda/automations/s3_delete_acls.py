
"""
This automation Deletes S3 Bucket Access Control Lists, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to delete S3 ACLS

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

  client.put_bucket_acl(
    Bucket=bucket_name,
    ACL='private'
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete S3 ACLs",
    "description": "Deletes S3 Bucket Access Control Lists",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO