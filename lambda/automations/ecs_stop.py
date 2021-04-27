"""ECS Stop

This automation attempts to stop running tasks in an ECS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
from automations.ecs_reboot import *

def stop_instance(client, target_cluster: str, target_instance: str) -> str:
  """ Attempts to stop the ECS instance

  Parameters
  ----------
  client : object
    The boto session tclient object
  target_cluster : str
    Cluster ID to perform automations on
  target_instance : str
    The ECS Instance to stop

  Returns
  -------
  string
    A string containing the status of the request

  """

  try:
    client.update_container_instance_state(
      cluster=target_cluster,
      containerInstances=[target_instance],
      status='DRAINING'
    )

    automation_output = "ECS Instance: {} stopped successfully".format(target_instance)

  except ClientError as err:
    automation_output = "An unexpected Client Error occured, error: {}".format(err)

  return automation_output


def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to reboot running ecs tasks

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ecs')

  cluster_arn = resource['arn']
  role_arn = automation_params.get('Role')

  ## Get a list of running tasks for the cluster
  try:
    running_tasks = client.list_tasks(
      cluster=cluster_arn,
      desiredStatus='RUNNING'
    )['taskArns']

  except ClientError as err:
    return "An unexpected CLient Error has occured, cannot gat list of running tasks. Error: {}".format(err)

  if len(running_tasks) != 0:
    for task in running_tasks:
      described_task = client.describe_tasks(
        cluster=cluster_arn,
        tasks=[task, ]
      )['running_tasks'][0]

      task_definition = described_task.get('taskDefinitionArn')

      definition = client.describe_task_definition(
        taskDefinition=task_definition
      )['taskDefinition']

      if definition.get('executionRoleArn') == role_arn:
        if 'EC2' in described_task.get('launchType'):
          automation_output = stop_instance(
            client=client,
            target_cluster=cluster_arn,
            target_instance=described_task.get('containerInstanceArn')
          )

        if 'error' in automation_output:
          return automation_output

        automation_output += ecs_stop_tasks(
          client=client,
          target_cluster=cluster_arn,
          task=task
        )

        if 'error' in automation_output:
          return automation_output

  if automation_output == '':
    automation_output = "No Running Tasks, Exiting..."

  return automation_output

  def info() -> dict:
    INFO = {
      "displayName": "Stop ECS Cluster",
      "description": "Stops ECS Cluster",
      "resourceTypes": [
        "ECS Cluster"
      ],
      "params": [
        {
          "name": "Role",
          "type": "string",
          "default": " "
        }
      ]
    }

    return INFO