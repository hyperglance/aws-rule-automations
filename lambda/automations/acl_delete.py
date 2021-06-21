"""
This automation Deletes an Access Control list, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to delete an Access Control List

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('ec2')
  acl_id = resource['attributes']['Network ACL ID']

  client.delete_network_acl(
    NetworkAclId=acl_id
  )

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