## dynamo_delete_table

## Deletes a Dynamo DB Table identified by configured Hyperglance Rule
import boto3
from botocore.exceptions import ClientError

## Delets Dynamo DB Table
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('dynamodb')
  table_name = entity['id']

  try:
    response = client.delete_table(
      TableName=table_name
    )
    action_output = "Deleted Dynamo DB Table: {}".format(table_name)

  except ClientError as err:
    action_output = "An unexpected error occured, error message {}".format(err)

  return action_output