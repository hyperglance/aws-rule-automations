"""RDS Aurora Delete Cluster

This action Deletes an Aurora backed RDS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os
import uuid

## Delete RDS Aurora DB Cluster
def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Delete and Aurora Backed RDS Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('rds')
  rds_instance = resource_id

  response = client.delete_db_cluster(
    DBClusterIdentifier=rds_instance,
    SkipFinalSnapshot=action_params.get('SkipAuroraSnapshot').lower() in ['true', 'y', 'yes'],
    FinalDBSnapshotIdentifier='Snapshot_{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance')))
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(result)
  else:
    action_output = "Deleted Autora Cluster: {}".format(rds_instance)

  return action_output


def info() -> str:
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