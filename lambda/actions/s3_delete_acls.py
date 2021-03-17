
"""
This action Deletes S3 Bucket Access Control Lists, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ], action_params = '') -> str:
  """ Attempts to delete S3 ACLS

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on
  table : list
    A list of additional resource values that may be required

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('s3')
  bucket_name = resource_id

  try:
    bucket_acl = client.get_bucket_acl(Bucket=bucket_name)['Grants']

    if len(bucket_acl) == 2:
      action_ouput = "Only found the default Canonical User ACL: {}, nothing to do".format(bucket_acl[0])
      return action_ouput

  try:
    response = client.put_bucket_acl(
      Bucket=bucket_name,
      ACL='private'
      )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_ouput = "An unexpected error occured, error message: {}".format(result)
    else:
      action_ouput = "ACLs: {} removed from bucket: {}".format(bucket_acl[1:], bucket_name)

  except ClientError as err:
    action_ouput = "An unexpected client error occured, error: {}".format(err)

  return action_ouput


def info() -> str:
  INFO = {
    "displayName": "Delete S3 ACLs",
    "description": "Deletes S3 Bucket Access Control Lists",
    "resourceTypes": [
      "S3",
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO