"""S3 Enable Logging

This automation Enables server access logging, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Create an S3 Bucket for Logging

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  s3_client = boto_session.client('s3')
  s3_resource = boto_session.resource('s3')

  bucket_name =  resource['id']
  account_id = resource['account']
  region_id = resource['region']

  logging_bucket = s3_resource.BucketLogging(bucket_name)
  target_log_bucket = account_id + "s3accesslogs" + region_id

  ## Check if the bucket exists...
  try:
    s3_client.head_bucket(
      Bucket=target_log_bucket
    )

  except:
    ## Bucket doesn't exists, or permissions are invalid, try creating it
    # LocationConstraint should not be set for us-east-1
    # LocationConstraint should not be set to EU for eu-west-1
    if region_id == "us-east-1":
      s3_client.create_bucket(
        Bucket=target_log_bucket,
        ACL='log-delivery-write'
      )
    else:
      s3_client.create_bucket(
        Bucket=target_log_bucket,
        CreateBucketConfiguration={
          'LocationConstraint':  "EU" if region_id == "eu-west-1" else region_id
        },
        ACL='log-delivery-write'
      )

  logging_bucket.put(
    BucketLoggingStatus={
      'LoggingEnabled': {
        'TargetBucket': target_log_bucket,
        'TargetPrefix': ''
      }
    }
  )


def info() -> dict:
  INFO = {
    "displayName": "Enable Access Logging",
    "description": "Enables Access Logging for S3 Buckets",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ],
    "permissions": [
      "s3:ListBucket",
      "s3:CreateBucket",
      "s3:PutBucketLogging"
    ]
  }

  return INFO