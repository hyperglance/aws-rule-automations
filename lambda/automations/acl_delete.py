"""
This automation Deletes an Access Control list, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to delete an Access Control List

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

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
    automation_output = "Network ACL: {} deleted".format(acl_id)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output

def info() -> dict:
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