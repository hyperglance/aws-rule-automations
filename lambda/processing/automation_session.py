"""Gets Boto Session for Cross Account automations

Returns Boto Session
"""

import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

## Get some details about where this lambda is running
identity = boto3.client('sts').get_caller_identity()
this_account_id = identity['Account']
partition = identity['Arn'].split(':')[1]
logger.debug('Got the account: %s', this_account_id)

def get_boto_session(target_account_id: str, target_region: str='us-east-1') -> object:
  if target_account_id == this_account_id:
    ## It's the same account, grab the session
    logger.info('Resource is local to this account')
    return boto3.Session(region_name=target_region)

  hyperglance_role = f'arn:{partition}:iam::{target_account_id}:role/Hyperglance_Automations'
  logger.info('Role ARN to use: %s', hyperglance_role)

  ## Try and get the credentials for ENV
  try:
    automation_credentials = globals()['automation_account_session_creds'][target_account_id]
  except (NameError, KeyError, DeprecationWarning):
    ## Likely first time we have tried to acquire, creentials, lets assume the role
    global automation_account_session_creds
    automation_account_session_creds = {}
    client = boto3.client('sts')

    try:
      automation_role = client.assume_role(
        RoleArn=hyperglance_role,
        RoleSessionName='HyperglanceAutomations'
      )

      ## Get cresential to use in automation
      automation_credentials = automation_role['Credentials']
      automation_account_session_creds[target_account_id] = automation_credentials

      logger.info('Assumed role: %s', hyperglance_role)

    except ClientError as err:
      if err.response['Error']['Code'] == 'AccessDenied':
        raise RuntimeError('Unable to Assume role on account: %s, please check that the role exists on the target account', target_account_id)
      else:
        raise RuntimeError('An unexpected error occured attempting to assume role for account: %s', target_account_id)

  return boto3.Session(
    aws_access_key_id=automation_credentials['AccessKeyId'],
    aws_secret_access_key=automation_credentials['SecretAccessKey'],
    aws_session_token=automation_credentials['SessionToken'],
    region_name=target_region
  )
