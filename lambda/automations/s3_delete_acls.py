
"""
This automation Deletes S3 Bucket Access Control Lists, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to delete S3 ACLS

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
    bucket_acl = client.get_bucket_acl(Bucket=bucket_name)['Grants']

    if len(bucket_acl) == 2:
      automation_ouput = "Only found the default Canonical User ACL: {}, nothing to do".format(bucket_acl[0])
      return automation_ouput

    response = client.put_bucket_acl(
      Bucket=bucket_name,
      ACL='private'
      )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      automation_ouput = "An unexpected error occured, error message: {}".format(result)
    else:
      automation_ouput = "ACLs: {} removed from bucket: {}".format(bucket_acl[1:], bucket_name)

  except ClientError as err:
    automation_ouput = "An unexpected client error occured, error: {}".format(err)

  return automation_ouput


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