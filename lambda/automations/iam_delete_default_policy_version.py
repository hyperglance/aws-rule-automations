"""
This automation Deletes defauly policy version, and sets it to latest version, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to delete default policy and set to the LATEST

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
  policy_arn = resource['attributes']['Policy ARN']

  ## Get current default version
  default_version_id = client.get_policy(PolicyArn=policy_arn) ['Policy']['DefaultVersionId']

  ## Get current versions
  policy_versions = client.list_policy_versions(
    PolicyArn=policy_arn
  ) ["Versions"]

  ## If default version is not the only version, then use latest version
  if len(policy_versions) > 1:
    ## Get the last version number
    new_version_id = policy_versions[1] if policy_versions[0]['IsDefaultVersion'] else policy_versions[0]

    client.set_default_policy_version(
      PolicyArn=policy_arn,
      VersionId=new_version_id
    )

    client.delete_policy_version(
      PolicyArn=policy_arn,
      VersionId=default_version_id
    )


def info() -> dict:
  INFO = {
    "displayName": "Delete Default Policy Version",
    "description": "Deletes the default policy version, and sets latest version as active",
    "resourceTypes": [
      "IAM Policy"
    ],
    "params": [

    ]
  }

  return INFO