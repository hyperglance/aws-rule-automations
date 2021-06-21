"""IAM Attach Policy to Role

This automation attaches a policy to an IAM Role, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to attach an IAM policy to an IAM Role

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.cliet('iam')

  role_arn = resource['attributes']['Role ARN']
  policy_arn = automation_params.get('Policy')

  client.attach_role_policy(
    RoleName=role_arn,
    PolicyArn=policy_arn
  )


def info() -> dict:
  INFO = {
    "displayName": "Attach policy to Role",
    "description": "Attaches an existing policy to an IAM role.",
    "resourceTypes": [
      "IAM"
    ],
    "params": [
      {
        "name": "Policy",
        "type": "string",
        "default": ""
      }
    ]
  }

  return INFO