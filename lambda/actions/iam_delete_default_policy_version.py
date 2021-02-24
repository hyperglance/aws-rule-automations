"""
This action Deletes defauly policy version, and sets it to latest version, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def delete_policy_version(client, policy_arn: str, policy_version_id: str) -> str:
  """ Deletes the specified default policy version

  Parameters
  ----------
  client: object
    The boto client to use for the request
  policy_arn : str
    The target policy arn
  policy_version_id: str
    The target policy version id

  Returns
  -------
  string
    A string containing the action result

  """

  response = client.delete_policy_version(
    PolicyArn=policy_arn,
    VersionId=policy_version_id
  )

  return "Policy version: {} deleted"

def policy_last_version(policy_versions: list) -> str:
  """ Gets the last version of the policy

  Parameters
  ----------
  policy_arn : str
    The policy arn of the target policy

  Returns
  -------
  string
    A string containing the version ID

  """
  if (policy_versions[0]['IsDefaultVersion'] == False):
    return policy_versions[0]['VersionId']
  else:
    return policy_versions[1]['VersionId']

def policy_replace_default_version(client, policy_arn: str, new_id: str) -> str:
  """ Replaces the default policy version

  Parameters
  ----------
  client: object
    The boto client to use for the request
  policy_arn : str
    The policy arn of the Policy to replace the version
  new_id: str
    The new policy version ID to use

  Returns
  -------
  string
    A string containing the action result

  """
  response = client.set_default_policy_version(
    PolicyArn=policy_arn,
    VersionId=new_id
  )
  return "Policy version for Policy: {}, set to: {}".format(policy_arn, new_id)

def policy_default_version_id(client, policy_arn: str) -> str:
  """ Gets the current default version id

  Parameters
  ----------
  client: object
    The boto client to use for the request
  policy_arn : str
    The policy arn of the Policy to check

  Returns
  -------
  string
    A string containing the action result

  """
  version_id = client.get_policy(PolicyArn=policy_arn) ['Policy']['DefaultVersionId']
  return version_id

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
  policy_arn = resource_id

  ## Get current default version
  policy_default_version_id = policy_default_version_id(client=client, policy_arn=policy_arn)

  ## Get current versions
  policy_versions = client.list_policy_versions(
    PolicyArn=policy_arn
  ) ["Versions"]

  ## If default version is not the only version, then use latest version
  if len(policy_versions) > 1:
    ## Get the last version number
    new_version_id = policy_last_version(policy_versions=policy_versions)

    action_output = policy_replace_default_version(client=client, policy_arn=policy_arn, new_id=new_version_id)
    action_output += delete_policy_version(client=client, policy_arn=policy_arn, policy_version_id=policy_default_version_id)

  else: ## User default version
    action_output = "There are no other version other than default for policy: {}".format(policy_arn)

  return action_output