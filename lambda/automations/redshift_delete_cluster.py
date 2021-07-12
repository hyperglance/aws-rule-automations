"""Redshift Delete Cluster

This automation Deletes a Redshift Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import uuid

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts Delete a Redshift Cluster

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('redshift')
  cluster = resource['id']

  client.delete_cluster(
    ClusterIdentifier=cluster,
    SkipFinalClusterSnapshot=automation_params.get('SkipSnapshot').lower() in ['true', 'y', 'yes'],
    FinalClusterSnapshotIdentifier='Snapshot-{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance'))),
    FinalClusterSnapshotRetentionPeriod=-1
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete Redshift Cluster",
    "description": "Deletes a Redshift Cluster",
    "resourceTypes": [
      "Redshift Cluster"
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