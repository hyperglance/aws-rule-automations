"""S3 Enable Logging

This automation Enables server access logging, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Create an S3 Bucket for Logging

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  sts_client = boto_session.client('sts')
  boto_session = boto_session.Session()

  s3_client = boto_session.client('s3')
  s3_resource = boto_session.resource('s3')

  bucket_name =  resource_id
  account_id = sts_client.get_caller_identity()["Account"]
  region_id = boto_session.region_name

  logging_bucket = s3_resource.BucketLogging(bucket_name)
  target_log_bucket = account_id + "s3accesslogs" + region_id

  ## Check if the bucket exists...
  try:
    s3_client.head_bucket(
      Bucket=target_log_bucket
    )

  except ClientError:
    ## Bucket doesn't exists, or permissions are invalid, try creating it
    try:
      if region_id == "us-east-1":
        response = s3_client.create_bucket(
          Bucket=target_log_bucket,
          ACL='log-delivery-write'
        )
      elif region_id == "eu-west-1":
        region_id = "EU"
        response = s3_client.create_bucket(
          Bucket=target_log_bucket,
          CreateBucketConfiguration={
            'LocationConstraint': region_id
          },
          ACL='log-delivery-write'
        )
      else:
        response = s3_client.create_bucket(
          Bucket=target_log_bucket,
          CreateBucketConfiguration={
            'LocationConstraint': region_id
          },
          ACL = 'log-delivery-write'
        )

      result = response['ResponseMetadata']['HTTPStatusCode']
      if result >= 400:
        automation_output = "An unexpected error has occured, error: {}".format(result)
      else:
        automation_output = "Logging bucket created: {}".format(target_log_bucket)

    except ClientError as err:
      automation_output = "An unexpectd Client Error has occured, error: {}".format(err)


  response = logging_bucket.put(
    BucketLoggingStatus={
      'LoggingEnabled': {
        'TargetBucket': target_log_bucket,
        'TargetPrefix': ''
      }
    }
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    automation_output += "An unexpected error occured when enabling bucket logging, error: {}".format(result)
  else:
    automation_output += "Bucket logging enabled from bucket: {} to bucket: {}".format(bucket_name, target_log_bucket)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Enable Access Logging",
    "description": "Enables Access Logging for S3 Buckets",
    "resourceTypes": [
      "S3 Bucket"
    ],
    "params": [

    ]
  }

  return INFO