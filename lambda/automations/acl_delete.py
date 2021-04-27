"""
This automation Deletes an Access Control list, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to delete an Access Control List

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

  client = boto_session.client('ec2')
  acl_id = resource['attributes']['Network ACL ID']

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