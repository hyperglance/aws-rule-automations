"""
This action deletes all ACLs and Bucket policies from and S3 bucket, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import actions.s3_delete_acls

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to ACLS and Policies from an S3 bucket

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('s3')
  bucket_name = resource_id

  try:
    ## Remove bucket policy
    response = client.delete_bucket_policy(
      Bucket=bucket_name
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_ouptut = "An unexpected error occured deleting the bucket policy for bucket: {}, error:".format(bucket_name, result)
    else:
      action_ouptut = "Bucket policy successully removed from bucket: {}".format(bucket_name)

  except ClientError as err:
    if err.response['Error']['Code'] == 'NoSuchBucketPolicy':
      action_ouptut = "Bucket: {} does not have a bucket policy.".format(bucket_name)
    else:
      action_ouptut = "An unexpected client error occured, error: {}".format(err)

  ## Use existing action s3_delete_acls to delelte bucket ACLs and keep code DRY
  s3_delete_acls = s3_delete_acls()

  try:
    action_ouptut += s3_delete_acls(
      boto_session=boto_session,
      resource_id=resource_id
    )

  return action_ouptut


def info() -> dict:
  INFO = {
    "displayName": "Delete S3 Permissions",
    "description": "Deletes all ACLs and Bucket Policies from an S3 bucket",
    "resourceTypes": [
      "S3",
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO