"""S3 Allow SSL Only

This automation enforces S3 Encryption of Data Transfers using SSL, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import json
import logging



def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to set an SSL Policy on an S3 Bucket

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
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::{}:root"
                },
                "Action": "s3*",
                "Resource": "arn:aws:s3:::{}/*"
            },
            {
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::{}/*",
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            }

        ]
    }

    bucket_name = resource['id']
    account_number = resource['account']

    bucket_policy['Statement'][0]['Principal']['AWS'] = bucket_policy['Statement'][0]['Principal']['AWS'].format(account_number)
    bucket_policy['Statement'][0]['Resource'] = bucket_policy['Statement'][0]['Resource'].format(bucket_name)
    bucket_policy['Statement'][1]['Resource'] = bucket_policy['Statement'][1]['Resource'].format(bucket_name)

    policy = json.dumps(bucket_policy)
    s3 = boto_session.resource('s3')
    bucket_policy = s3.BucketPolicy(bucket_name)

    bucket_policy.put(
        Policy=policy
    )


def info() -> dict:
    INFO = {
        "displayName": "S3 Enforce SSL",
        "description": "Enforces SSL for object access",
        "resourceTypes": [
            "S3 Bucket"
        ],
        "params": [

        ],
        "permissions": [
            "s3:PutBucketPolicy"
        ]
    }

    return INFO
