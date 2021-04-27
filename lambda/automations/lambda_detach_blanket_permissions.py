"""
This automation detaches a lambda execution policy with blanket permissions, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError


def policies(policy) -> list:
  """ Attempts to enumerate the policies and check for blanket resources

  Parameters
  ----------
  policy : string
    The target execution policy

  Returns
  -------
  list
    A list of arns to a ction

  """

  arn_ids = []

  try:
    for policyName in policy['combinedPolicies']:
      for Statement in policyName['policyDocument']['Statement']:
        if Statement['Effect'] == "Allow" and 'Resource' in Statement and "*" in str(Statement['Resource']):
          arn_ids.append(policyName['id'])
    
    ## Remove any duplicates
    arn_ids = list(dict.fromkeys(arn_ids))

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)
    return automation_output

  return arn_ids


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to delete a User Access Key

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
  
  policy = resource['attributes']['Policy Name']
  execution_role = policy.get('name')
  
  try:
    arn_ids = policies(policy=policy)

    for policy in arn_ids:
      try:
        client.detach_role_policy(
          RoleName=execution_role,
          PolicyArn=policy
        )

        automation_output = "Detached policy: {} from execution role: {}".format(policy.split('/')[-1], execution_role)

      except ClientError as err:
        automation_output = "An unexpected client error has occured, error: {}".format(err)

  except ClientError as err:
    automation_output = "An unexpected client error has occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Detach Lambda Permissions",
    "description": "Detaches Permissions from a Lambda execution role, that allows ALL (*) resources",
    "resourceTypes": [
      "IAM"
    ],
    "params": [

    ]
  }

  return INFO