"""Gets Boto Session for Cross Account automations

Returns Boto Session
"""

import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_boto_session(target_account_id: str, target_region: str='us-east-1') -> object:
  """ Attempts to Delete and EBS Volume

  Parameters
  ----------
  target_account_id : string
    The account id to use in the session request
  target_region : string, required: no
    Region for credential session, default to 'us-east-1' if no va;ie is passed

  Returns
  -------
  session
    Service Client Instance

  """

  hyperglance_role = "arn:aws:iam::" + target_account_id + ":role/Hyperglance_automations"
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
      automation_account_session_creds[target_account_id] = automation_role['Credentials']
      automation_credentials = automation_account_session_creds[target_account_id]

      logger.info('Assumed role: %s', hyperglance_role)

    except ClientError as err:
      if err.response['Error']['Code'] == 'AccessDenied':
        logger.error('Unable to Assume role on account: %s, please check that the role exists on the target account', target_account_id)
      else:
        logger.error('An unexpected error occured attempting to assume role for account: %s', target_account_id)

  boto_session = boto3.Session(
    aws_access_key_id=automation_credentials['AccessKeyId'],
    aws_secret_access_key=automation_credentials['SecretAccessKey'],
    aws_session_token=automation_credentials['SessionToken'],
    region_name=target_region
  )

  return boto_session