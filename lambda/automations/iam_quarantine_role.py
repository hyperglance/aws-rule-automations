"""IAM Quarantine Role

This automation Quarantines and IAM Role, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import json

POLICY_NAME = 'hyperglance_quarantine_rules'
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
  """ Attempts to attach an IAM policy to an EC2 Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  role_arn = resource['id']

  policy_arn = role_arn.replace(':role/', ':policy/') + '_role_quarantined_by_hyperglance'

  client = boto_session.client('iam')

  try:
    client.create_policy(
      PolicyName=POLICY_NAME,
      PolicDocument=DENY_POLICY
    )
  except:
    pass # Policy might already exist

  client.attach_role_policy(
    RoleName=role_arn,
    PolicyArn=policy_arn
  )


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
