"""EC2 Delete Key Pair

This action Deletes a Key Pair, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import boto3
from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to Delete a Key Pair

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

  client = boto_session.client('ec2')
  keypair = resource_id

  try:
    response = client.delete_key_pair(
      KeyName=keypair
    )

    action_output = "KeyPair {} was deleted successfully".format(keypair)

  except ClientError as err:
    action_output = "An unexpected error occured, error message: {}".format(err)

  return action_output