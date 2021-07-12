"""RDS Terminate Instance

This automation Deletes and RDS DB Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import uuid

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete and RDS DB Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('rds')

  rds_instance = resource['id']

  client.delete_db_instance(
    DBInstanceIdentifier=rds_instance,
    SkipFinalSnapshot=automation_params.get('SkipSnapshot').lower() in ['true', 'y', 'yes'],
    FinalDBSnapshotIdentifier='Snapshot-{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance'))),
    DeleteAutomatedBackups=automation_params.get('DeleteBackups').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete RDS DB Instance",
    "description": "Deletes an RDS DB Instance",
    "resourceTypes": [
      "RDS DB Instance"
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