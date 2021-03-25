"""RDS Aurora Delete Cluster

This automation Deletes an Aurora backed RDS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import os
import uuid

## Delete RDS Aurora DB Cluster
def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Delete and Aurora Backed RDS Instance

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

  response = client.delete_db_cluster(
    DBClusterIdentifier=rds_instance,
    SkipFinalSnapshot=automation_params.get('SkipAuroraSnapshot').lower() in ['true', 'y', 'yes'],
    FinalDBSnapshotIdentifier='Snapshot_{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance')))
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    automation_output = "An unexpected error occured, error message: {}".format(result)
  else:
    automation_output = "Deleted Autora Cluster: {}".format(rds_instance)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Delete Aurora Cluster",
    "description": "Deletes and Aurora DB Cluster",
    "resourceTypes": [
      "RDS"
    ],
    "params": [
      {
        "name": "SkipAuroraSnapshot",
        "type": "bool",
        "default": "False"
      }
    ]
  }

  return INFO