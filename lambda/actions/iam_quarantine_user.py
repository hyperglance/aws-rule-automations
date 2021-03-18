"""
This action Quarantines and IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import json


def create_policy(boto_session) -> str:
  """ Attempts to create the deny policy

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')

  policy = {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Deny",
        "Action": "*",
        "Resource": "*"
      }
    ]
  }

  response = client.create_policy(
    PolicyName='hyperglance_quarantine_deny_policy',
    PolicyDocument=json.dumps(policy)
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error: {}".format(response)
  else:
    action_output = "Quarantine IAM Policy Created"

  return action_output


def deny_policy_exists(boto_session, policy_arn: str) -> str:
  """ Attempts to check if the Deny Policy exists, creates it if it doesn't

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  policy_arn : str
    The policy arn to check

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')

  try:
    response = client.get_policy(
      PolicyArn=policy_arn
    )

    if response['ResponseMetadata']['HTTPStatusCode'] < 400:
      action_output = "Policy already exists"

  except ClientError as err:
    if err.response['Error']['Code'] == 'NoSuchEntity':
      ## Create the Policy
      action_output = create_policy(
        boto_session=boto_session
      )
    else:
      action_output = "An unexpected client error occured, error: {}".format(err)

  return action_output


def attach_user_policy(boto_session, policy_arn: str, user: str) -> str:
  """ Attempts to attach the policy to a user

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  policy_arn : str
    The policy to attach
  user : str
    User to attach the policy to

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')

  try:
    response = client.attach_user_policy(
      UserName=user,
      PolicyArn=policy_arn
    )
    action_output = "Deny policy attached to user: {}".format(user)

  except ClientError as err:
    action_output = "An unexpected client error has occured, error: {}".format(err)

  return action_output


def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to attach a qurantine policy to a user

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

  client = boto_session.client('iam')
  
  account_id = table[0]['Account ID']
  user_name = resource_id
  deny_policy_arn = "arn:aws:iam:{}:policy/hyperglance_quarantine_deny_policy".format(account_id)

  try:
    action_output = deny_policy_exists(
      boto_session=boto_session
    )

    action_output += attach_user_policy(
      boto_session=boto_session,
      policy_arn=deny_policy_arn
    )

  except ClientError as err:
    action_output = "An unexpected client error has occured. error: {}".format(err)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Quarantine User",
    "description": "Attaches a DENY ALL policy to the user",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO