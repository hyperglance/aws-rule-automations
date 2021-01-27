## rds_aurora_delete_cluster

## Deletes and optionally Snapshots abd RDS Aurora Cluster
import os
import uuid
from boto3 import session, rds

## Delete DB Cluster
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('rds')
  rds_instance = entity['id']

  response = client.delete_db_cluster(
    DBClusterIdentifier=rds_instance,
    SkipFinalSnapshot=os.environ['SkipAuroraSnapshot'],
    FinalDBSnapshotIdentifier='Snapshot_{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance')))
  )

  result = response['ResponseMetadata']['HTTPStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(str(result))
  else:
    action_output = "Deleted Autora Cluster: {}".format(rds_instance)

  return action_output