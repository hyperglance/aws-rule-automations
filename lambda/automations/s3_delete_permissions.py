"""
This automation deletes all ACLs and Bucket policies from and S3 bucket, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import automations.s3_delete_acls

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to ACLS and Policies from an S3 bucket

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

  ## Remove bucket policy
  client.delete_bucket_policy(
    Bucket=bucket_name
  )

  ## Use existing automation s3_delete_acls to delelte bucket ACLs and keep code DRY
  automations.s3_delete_acls.hyperglance_automation(
    boto_session=boto_session,
    resource=resource,
    automation_params=automation_params
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete S3 Permissions",
    "description": "Deletes all ACLs and Bucket Policies from an S3 bucket",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ],
    "permissions": [
      "s3:DeleteBucketPolicy",
      "s3:PutBucketAcl"
    ]
  }

  return INFO