"""
This action Deletes an Access Control list, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to delete an Access Control List

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
  acl_id = resource_id

  try:
    client.delete_network_acl(
      NetworkAclId=acl_id
    )
    action_output = "Network ACL: {} deleted".format(acl_id)

  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)

  return action_output