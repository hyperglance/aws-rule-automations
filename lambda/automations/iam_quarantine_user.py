"""
This automation Quarantines and IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import json


def create_policy(boto_session) -> str:
  """ Attempts to create the deny policy

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation

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
        "automation": "*",
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
    automation_output = "An unexpected error occured, error: {}".format(response)
  else:
    automation_output = "Quarantine IAM Policy Created"

  return automation_output


def deny_policy_exists(boto_session, policy_arn: str) -> str:
  """ Attempts to check if the Deny Policy exists, creates it if it doesn't

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
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
      automation_output = "Policy already exists"

  except ClientError as err:
    if err.response['Error']['Code'] == 'NoSuchEntity':
      ## Create the Policy
      automation_output = create_policy(
        boto_session=boto_session
      )
    else:
      automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output


def attach_user_policy(boto_session, policy_arn: str, user: str) -> str:
  """ Attempts to attach the policy to a user

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
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
    automation_output = "Deny policy attached to user: {}".format(user)

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to attach a qurantine policy to a user

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')
  
  account_id = resource['account']
  user_name = resource['attributes']['User Name']
  deny_policy_arn = "arn:aws:iam:{}:policy/hyperglance_quarantine_deny_policy".format(account_id)

  try:
    automation_output = deny_policy_exists(
      boto_session=boto_session,
      policy_arn=deny_policy_arn
    )

    automation_output += attach_user_policy(
      boto_session=boto_session,
      policy_arn=deny_policy_arn,
      user=user_name
    )

  except ClientError as err:
    automation_output = "An unexpected client error has occured. error: {}".format(err)

  return automation_output


def info() -> dict:
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