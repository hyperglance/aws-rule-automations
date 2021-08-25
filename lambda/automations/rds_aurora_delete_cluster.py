"""RDS Aurora Delete Cluster

This automation Deletes an Aurora backed RDS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


## Delete RDS Aurora DB Cluster
def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to Delete and Aurora Backed RDS Instance

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

    skip_snapshot = automation_params.get('SkipAuroraSnapshot').lower() in ['true', 'y', 'yes']

    response = client.describe_db_clusters(
        DBClusterIdentifier=resource['id']
    )

    cluster_members = response['DBClusters'][0]['DBClusterMembers']


    db_identifiers = [db['DBInstanceIdentifier'] for db in cluster_members]


    for identifier in db_identifiers:
        response = client.delete_db_instance(
            DBInstanceIdentifier=identifier
        )
    response = client.modify_db_cluster(
        DBClusterIdentifier=rds_instance,
        ApplyImmediately=True,
        DeletionProtection=False
    )
    try:
        client.delete_db_cluster(
            DBClusterIdentifier=rds_instance,
            SkipFinalSnapshot=skip_snapshot,
            FinalDBSnapshotIdentifier=None if skip_snapshot else 'Snapshot-{}'.format(
                str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance')))
        )
    except:
        client.delete_db_cluster(
            DBClusterIdentifier=rds_instance,
            SkipFinalSnapshot=True
        )


def info() -> dict:
    INFO = {
        "displayName": "Delete Aurora Cluster",
        "description": "Deletes and Aurora DB Cluster",
        "resourceTypes": [
            "Aurora DB Cluster"
        ],
        "params": [
            {
                "name": "SkipAuroraSnapshot",
                "type": "boolean",
                "default": "false"
            }
        ],
        "permissions": [
            "rds:DeleteDBCluster",
            "rds:DescribeDBClusters",
            "rds:ModifyDBCluster"
        ]
    }

    return INFO
