"""IAM Attach Policy to User

This automation attaches a policy to an IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to attach an IAM policy to an IAM User

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

  user_name = resource['attributes']['user name']
  policy_arn = automation_params.get('Policy')

  client.attach_user_policy(
    UserName=user_name,
    PolicyArn=policy_arn
  )

def info() -> dict:
  INFO = {
    "displayName": "Attach policy to User",
    "description": "Attaches an existing policy to an IAM User.",
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