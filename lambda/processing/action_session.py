"""Gets Boto Session for Cross Account Actions

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

  hyperglance_role = "arn:aws:iam::" + target_account_id + ":role/Hyperglance_Actions"
  logger.info('Role ARN to use: %s', hyperglance_role)

  ## Try and get the credentials for ENV
  try:
    action_credentials = globals()['action_account_session_creds'][target_account_id]
  except (NameError, KeyError, DeprecationWarning):
    ## Likely first time we have tried to acquire, creentials, lets assume the role
    global action_account_session_creds
    action_account_session_creds = {}
    client = boto3.client('sts')

    try:
      action_role = client.assume_role(
        RoleArn=hyperglance_role,
        RoleSessionName='HyperglanceActions'
      )

      ## Get cresential to use in action
      action_account_session_creds[target_account_id] = action_role['Credentials']
      action_credentials = action_account_session_creds[target_account_id]

      logger.info('Assumed role: %s', hyperglance_role)

    except ClientError as err:
      if err.response['Error']['Code'] == 'AccessDenied':
        logger.error('Unable to Assume role on account: %s, please check that the role exists on the target account', target_account_id)
      else:
        logger.error('An unexpected error occured attempting to assume role for account: %s', target_account_id)

  boto_session = boto3.Session(
    aws_access_key_id=action_credentials['AccessKeyId'],
    aws_secret_access_key=action_credentials['SecretAccessKey'],
    aws_session_token=action_credentials['SessionToken'],
    region_name=target_region
  )

  return boto_session