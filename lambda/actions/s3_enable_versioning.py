"""S3 Enable Versioning

This action Enables versioning on S3 Buckets, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ], action_params = '') -> str:
  """ Attempts to Enable versioning on an S3 Bucket

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
    response = client.put_bucket_versioning(
      Bucket=bucket_name,
      VersioningConfiguration={
        'MFADelete': 'Disabled',
        'Status': 'Enabled'
      },
    )
    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "Bucket {} enabled for versioning".format(bucket_name)
    
  except ClientError as err:
    action_output = "An unexpected Client error Occured, error message: {}".format(err)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Enable S3 Versioning",
    "description": "Enables Object Versioning",
    "resourceTypes": [
      "S3",
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO