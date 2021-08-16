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

  skip_snapshot = automation_params.get('SkipSnapshot').lower() in ['true', 'y', 'yes']

  client.delete_db_instance(
    DBInstanceIdentifier=rds_instance,
    SkipFinalSnapshot=skip_snapshot,
    FinalDBSnapshotIdentifier=None if skip_snapshot else 'Snapshot-{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance'))),
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
        "type": "boolean",
        "default": "false"
      },
      {
        "name": "DeleteBackups",
        "type": "boolean",
        "default": "false"
      }
    ],
    "permissions": [
      "rds:DeleteDBInstance"
    ]
  }

  return INFO