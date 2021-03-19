"""Redshift Delete Cluster

This action Deletes a Redshift Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os
import uuid

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts Delete a Redshift Cluster

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

  client = boto_session.client('redshift')
  cluster = resource_id

  

  response = client.delete_cluster(
    ClusterIdentifier=cluster,
    SkipFinalSnapshot=action_params.get('SkipRedshiftSnapshot').lower() in ['true', 'y', 'yes'],
    FinalClusterIdentifier='Snapshot_{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance'))),
    FinalClusterSnapshotRetentionPeriod=-1
  )

  result = response['ResponseMetadata']['HttpStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(result)
  else:
    action_output = "Deleted Redshift Cluster: {}".format(cluster)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Delete Redshift Cluster",
    "description": "Deletes a Redshift Cluster",
    "resourceTypes": [
      "Redshift CLuster"
    ],
    "params": [
      {
        "name": "SkipSnapshot",
        "type": "bool",
        "default": "False"
      }
    ]
  }

  return INFO