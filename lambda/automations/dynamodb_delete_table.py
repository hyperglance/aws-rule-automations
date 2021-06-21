"""Dynamo DB Delete Table

This automation Deletes a Dynamo DB Table, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

## Delets Dynamo DB Table
def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete and Dynamo DB Table

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('dynamodb')
  table_name = resource['id']

  client.delete_table(
    TableName=table_name
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete Dynamo DB Table",
    "description": "Deletes a specified Dynamo DB Table",
    "resourceTypes": [
      "DynamoDB Table"
    ],
    "params": [

    ]
  }

  return INFO