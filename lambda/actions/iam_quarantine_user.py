"""
This action Quarantines and IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import json
from botocore.exceptions import ClientError


def set_deny_policy(client) -> str:
  return "policy"

def deny_policy_exists(client, policy_arn: str) -> bool:
  return True

def attach_user_policy(client, policy_arn: str, user: str) -> str:
  return "result"

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to delete default policy and set to the LATEST

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')
  account_id = resource_id

  action_output = "Not Implemented Yet"

  return action_output