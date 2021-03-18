"""
This action Deletes an Access Control list, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to delete an Access Control List

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

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

def info() -> str:
  INFO = {
    "displayName": "Delete ACL",
    "description": "Deletes and Access Control List",
    "resourceTypes": [
      "Network ACL"
    ],
    "params": [

    ]
  }

  return INFO