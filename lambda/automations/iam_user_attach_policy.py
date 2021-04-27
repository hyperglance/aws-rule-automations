"""IAM Attach Policy to User

This automation attaches a policy to an IAM User, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def attach_policy_to_user(client, user_name, policy_arn) -> str:
  """ Attempts to attach the policy to the role

  Parameters
  ----------
  client : object
    The boto IAM client
  role : str
    The role arn to attach the policy to.
  policy_arn : str
    arn of the policy to attach


  Returns
  -------
  string
    A string containing the status of the request

  """

  try:
    response = client.attach_user_policy(
      UserName=user_name,
      PolicyArn=policy_arn
    )
    automation_ouput = "Policy attached to user: {} successfully".format(user_name)

  except ClientError as err:
    automation_ouput = "An unexpected client error has occured, error: {}".format(err)

  return automation_ouput


def policy_exists(client, policy_arn):
  """ Checks if the defined policy Exists in the account

  Parameters
  ----------
  client : object
    The boto IAM client
  policy_arn : str
    arn of the policy to attach


  Returns
  -------
  string
    A string containing the status of the request
  bool
    Boolean indicating if policy was found in target acount

  """

  try:
    response = client.get_policy(
      PolicyArn=policy_arn
    )

    if response['ResponseMetadata']['HTTPStatusCode'] < 400:
      automation_output = "Policy exists in this account"
      found_policy = True
    
  except ClientError as err:
    if err.response['Error']['Code'] == 'NoSuchEntity':
      automation_output = "The specified policy {} does not exist, please provide a valud policy_arn".format(policy_arn)
      found_policy = False
    else:
      automation_output = "An unexpected client error has occured, error: {}".format(err)
      found_policy = False

  return automation_output, found_policy


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to attach an IAM policy to an IAM User

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

  user_name = resource['attributes']['user name']
  account_id = resource['account']
  policy_arn = automation_params.get('Policy')

  try:
    output, policy_exists = policy_exists(
      client=client,
      policy_arn=policy_arn
    )
    
    automation_output = output

    if policy_exists:
      automation_output += attach_policy_to_user(
        client=client,
        policy_arn=policy_arn
      )
    else:
      return automation_output

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output

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