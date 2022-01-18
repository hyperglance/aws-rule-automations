"""IAM Attach Policy to User

This automation attaches a policy to an IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
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
    user_name = resource['attributes']['User Name']
    policy_name = automation_params.get('Policy')
    policies = client.list_policies()['Policies']  # no specific API call to get policy by name

    policy_arn = ''

    for policy in policies:
        if policy_name == policy['PolicyName']:
            policy_arn = policy['Arn']
            break

    if policy_arn == '':
        logger.error("no such policy: " + policy_name)
        return

    client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )


def info() -> dict:
    INFO = {
        "displayName": "Attach policy to User",
        "description": "Attaches an existing policy to an IAM User",
        "resourceTypes": [
            "IAM User"
        ],
        "params": [
            {
                "name": "Policy",
                "type": "string",
                "default": ""
            }
        ],
        "permissions": [
            "iam:AttachUserPolicy",
            "iam:ListPolicies"
        ]
    }

    return INFO
