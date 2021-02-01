## redshift_delete_cluster

## Deletes a Redshift cluster identified by Configured Hyperglance Rules
import os
import uuid
import boto3

## Deletes RedShift Cluster
def hyperglance_action(boto_seesion, rule, entity, param):
  client = boto_session('redshift')
  cluster = entity['id']

  response = client.delete_cluster(
    ClusterIdentifier=cluster,
    SkipFinalSnapshot=os.environ['SkipRedshiftSnapshot'],
    FinalClusterIdentifier='Snapshot_{}'.format(str(uuid.uuid5(uuid.NAMESPACE_DNS, 'hyperglance'))),
    FinalClusterSnapshotRetentionPeriod=-1
  )

  result = response['ResponseMetadata']['HttpStatusCode']
  if result >= 400:
    action_output = "An unexpected error occured, error message: {}".format(str(result))
  else:
    action_output = "Deleted Redshift Cluster: {}".format(cluster)

  return action_output