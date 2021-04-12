"""RDS Terminate Instance

This automation Deletes and RDS DB Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import uuid

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Delete and RDS DB Instance

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

  client = boto_session.client('rds')

  rds_instance = resource_id

  try:
    response = client.delete_db_instance(
      DBInstanceIdentifier=rds_instance,
      SkipFinalSnapshot=automation_params.get('SkipSnapshot').lower() in ['true', 'y', 'yes'],
      FinalDBSnapsotIdentifier='Snapshot_{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance'))),
      DeleteAutomatedBackups=automation_params.get('DeleteBackups').lower() in ['true', 'y', 'yes']
    )
    automation_output = "Successfully deleted RDS DB Instance: {}".format(rds_instance)
  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Delete RDS DB Instance",
    "description": "Deletes an RDS DB Instance",
    "resourceTypes": [
      "RDS"
    ],
    "params": [
      {
        "name": "SkipSnapshot",
        "type": "bool",
        "default": "False"
      },
      {
        "name": "DeleteBackups",
        "type": "bool",
        "default": "False"
      }
    ]
  }

  return INFO