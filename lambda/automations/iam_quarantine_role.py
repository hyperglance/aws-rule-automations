"""IAM Quarantine Role

This automation Quarantines and IAM Role, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import json

def attach_policy_to_role(boto_session, role, policy_arn) -> str:
  """ Attempts to attach the deny policy to the role

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  role : str
    Role to attach the policy to
  policy_arn : 
    policy to attach

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session('iam')

  try:
    response = client.attach_role_policy(
      RoleName=role,
      PolicyArn=policy_arn
    )
    automation_output = "Deny policy successfully attached to role: {}".format(role)

  except ClientError as err:
    automation_output = "An unexpected client error occured when attaching policy, error: {}".format(err)

  return automation_output

def deny_policy_exists(boto_session, policy_arn: str) -> str:
  """ Attempts to check if a qurantine policy already exists

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  policy_arn: str
    ID of the policy to check

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
      automation_output = "Policy alread exists in target account"

  except ClientError as err:
    if err.response['Error']['Code'] == 'NoSuchEntity':
      create_deny_policy(
        boto_session=boto_session
      )
    else:
      automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output


def create_deny_policy(boto_session) -> str:
  """ Attempts to create a Deny Policy

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
  
  DENY_POLICY = {
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
    PolicyName='hyperglance_quarantine_deny_all_policy',
    PolicDocument=json.dumps(DENY_POLICY)
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    automation_output = "An unexpected error has occured, error: {}".format(response)
  else:
    automation_output = "Policy created successfully"

  return automation_output

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to attach an IAM policy to an EC2 Instance

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

  role_arn = resource['id']
  account_id = resource['account']

  policy_arn = "arn:aws:iam::{}:policy/hypergalnce_quarantine_deny_all_policy".format(account_id)

  try:
    automation_output = deny_policy_exists(
      boto_session=boto_session,
      policy_arn=policy_arn
    )

    automation_output += attach_policy_to_role(
      boto_session=boto_session,
      role=role_arn,
      policy_arn=policy_arn
    )

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Quarantine Role",
    "description": "Attaches a DENY ALL policy to the role",
    "resourceTypes": [
      "IAM"
    ],
    "params": [

    ]
  }

  return INFO
