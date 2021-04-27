"""S3 Allow SSL Only

This automation enforces S3 Encryption of Data Transfers using SSL, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import json


BUCKET_POLICY = {
  "Version": "2012-10-17",
  "Statement" : [

  ]
}

SSL_CHECK = {
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": "arn:aws:s3:::BUCKET_NAME/*",
  "Condition": {
    "Bool": {
      "aws:SecureTransport": "false"
    }
  }
}

GETPUT_CHECK = {
  "Effect": "Allow",
  "Principal": {
    "AWS": "ACCOUNT_NUMBER"
  },
  "Action": 'ACTION',
  "Resource": "arn:aws:s3:::BUCKET_NAME/*",
}


def has_get_put_action(bucket_policy) -> list:
  """ Checks if if the policy has any of the actions from the list

  Parameters
  ----------
  bucket_policy : list
    The current bucket policy

  Returns
  -------
  list
    Contain the actions

  """
  policy_statements = bucket_policy['Statement']
  actions = []
  action_options =[
    "s3:GetObject",
    "s3:*",
    "s3:PutObject",
    "s3:Put*",
    "s3:Get*",
    "*"
  ]

  for Statement in policy_statements:
    if Statement ["Effect"] == "Allow":
      if isinstance(Statement['Action'], list):
        actions = [actions for actions in Statement['Action'] if (actions in action_options)]
      elif Statement['Action'] in action_options:
        actions.append(Statement['Action'])

  return actions


def missing_action(action_options: list) -> str:
  """ Returns the missing Action in the policy statement

  Parameters
  ----------
  action_options : list
    The list of actions to compare against

  Returns
  -------
  str
    Contains the missing action

  """

  if ("*" in action_options) \
    or ("s3:*" in action_options) \
      or ('s3:GetObject' in action_options and 's3:PutObject' in action_options) \
        or ('s3:Get*' in action_options and 's3:Put*' in action_options) \
          or ('s3:GetObject' in action_options and 's3:Put*' in action_options) \
            or ('s3:Get*' in action_options and 's3:PutObject' in action_options):
    missing_action_option = 'ssl'

  elif 's3:GetObject' in str(action_options) \
    or "s3:Get*" in str(action_options):
    missing_action_option = 'Get'

  elif 's3:PutObject' in str(action_options) \
    or "s3:Put*" in str(action_options):
    missing_action_option = 'Put'

  return missing_action_option


def missing_statements(bucket_name: str, target_account: str, action_options: list) -> dict:
  """ Returns the statements that are missing from the policy

  Parameters
  ----------
  bucket_name : str
    The bucket name to apply the policy to
  target_account : str
    Account to use in the policy definition
  action_options : 
    The list of action options to compare against

  Returns
  -------
  dict
    A dict containing the policy statement

  """

  ## Get missing Policy Statement
  missing_policy_action = missing_action(
    action_options=action_options
  )

  if missing_policy_action == 'ssl':
    ## Add SSL Action
    SSL_CHECK["Resource"] = SSL_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)
    return SSL_CHECK, None

  elif missing_policy_action == 'Get':
    ## Add s3:PutObject action
    GETPUT_CHECK["Resource"] = GETPUT_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)
    GETPUT_CHECK["Principal"]["AWS"] = target_account
    GETPUT_CHECK["Action"] = "s3:PutObject"
    SSL_CHECK["Resource"] = SSL_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)

  elif missing_policy_action == 'Put':
    ## Add s3:GetObject action
    GETPUT_CHECK["Resource"] = GETPUT_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)
    GETPUT_CHECK["Principal"]["AWS"] = target_account
    GETPUT_CHECK["Action"] = "s3:GetObject"
    SSL_CHECK["Resource"] = SSL_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)

  else:
    ## Add both the Put and Get Object Actions
    GETPUT_CHECK["Resource"] = GETPUT_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)
    GETPUT_CHECK["Principal"]["AWS"] = target_account
    GETPUT_CHECK["Action"] = "s3*"
    SSL_CHECK["Resource"] = SSL_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)

  return GETPUT_CHECK, SSL_CHECK


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
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

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('s3')

  bucket_name = resource['id']
  account_number = resource['account']
  bucket_policy = resource['attributes']['policy']

  try:
    if bucket_policy == "null" or bucket_policy is None:
      ## No Policy - Create One
      GETPUT_CHECK["Resource"] = GETPUT_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)
      GETPUT_CHECK["Principal"]["AWS"] = account_number
      GETPUT_CHECK["Action"] = "s3*"
      SSL_CHECK["Resource"] = SSL_CHECK.get("Resource").replace("BUCKET_NAME", bucket_name)

      BUCKET_POLICY.get('Statement').append(GETPUT_CHECK)
      BUCKET_POLICY.get('Statement').append(SSL_CHECK)

      bucket_policy = BUCKET_POLICY

    else:
      ## Update the Policy with any Missing Actions
      policy_actions = has_get_put_action(
        bucket_policy=bucket_policy
      )

      add_getput, add_ssl = missing_statements(
        bucket_name=bucket_name,
        target_account=account_number,
        action_options=policy_actions
      )

      if add_ssl is None:
        ## Only add SSL
        bucket_policy['Statement'].append(add_ssl)
      else:
        ## Add SSL and GET / PUT
        bucket_policy['Statement'].append(add_getput)
        bucket_policy['Statement'].append(add_ssl)

    policy = json.dumps(bucket_policy)

    client.put_bucket_policy(
      Bucket=bucket_name,
      Policy=policy
    )

    automation_output = "Added SSL Policy to bucket: {}".format(bucket_name)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output

  def info() -> dict:
    INFO = {
      "displayName": "S3 Enforce SSL",
      "description": "Enforces SSL for object accedss",
      "resourceTypes": [
        "S3 Bucket"
      ],
      "params": [

      ]
    }

    return INFO