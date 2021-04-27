"""Dynamo DB Delete Table

This automation Deletes a Dynamo DB Table, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

## Delets Dynamo DB Table
def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to Delete and Dynamo DB Table

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

  client = boto_session.client('dynamodb')
  table_name = resource['id']

  try:
    response = client.delete_table(
      TableName=table_name
    )
    automation_output = "Deleted Dynamo DB Table: {}".format(table_name)

  except ClientError as err:
    automation_output = "An unexpected error occured, error message {}".format(err)

  return automation_output


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