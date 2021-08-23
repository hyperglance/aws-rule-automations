"""
This automation Quarantines and IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import json

from processing import automation_utils




POLICY_NAME = 'hyperglance_quarantine_users'
DENY_POLICY = json.dumps({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*"
    }
  ]
})


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to attach a qurantine policy to a user

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('iam')
  user_name = resource['attributes']['User Name']
  policy_arn = automation_utils.generate_arn('iam', POLICY_NAME, 'aws', resource['account'], '', '/', 'policy')

  try:
    response = client.create_policy(
      PolicyName=POLICY_NAME,
      PolicyDocument=DENY_POLICY
    )
  except:
    pass # Policy might already exist


  client.attach_user_policy(
    UserName=user_name,
    PolicyArn=policy_arn
  )


def info() -> dict:
  INFO = {
    "displayName": "Quarantine User",
    "description": "Attaches a DENY ALL policy to the user",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ],
    "permissions": [
      "iam:CreatePolicy",
      "iam:AttachUserPolicy"
    ]
  }

  return INFO