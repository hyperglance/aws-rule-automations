"""Dynamo DB Delete Table

This action Deletes a Dynamo DB Table, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

## Delets Dynamo DB Table
def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ]) -> str:
  """ Attempts to Delete and Dynamo DB Table

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on
  table : list
    A list of additional resource values that may be required

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('dynamodb')
  table_name = resource_id

  try:
    response = client.delete_table(
      TableName=table_name
    )
    action_output = "Deleted Dynamo DB Table: {}".format(table_name)

  except ClientError as err:
    action_output = "An unexpected error occured, error message {}".format(err)

  return action_output