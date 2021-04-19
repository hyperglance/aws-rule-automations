"""ECS Reboot

This automation attempts to reboot and ECS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def ecs_stop_tasks(client, target_cluster: str, task) -> str:
  """ Attempts to stop the running tasks

  Parameters
  ----------
  client : object
    The boto session client object
  target_cluster : str
    Target cluster
  task : str
    Task to try and stop

  Returns
  -------
  string
    A string containing the status of the request

  """

  try:
    client.stop_task(
      cluster=target_cluster,
      task=task,
      reason='Privileged tasks are dangerous'
    )
    automation_output = "Task: {} stopped successfully".format(task)

  except ClientError as err:
    automation_output = "An unexpected error occured, error: {}".format(err)

  return automation_output


def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to reboot running ecs tasks

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

  client = boto_session.client('ecs')

  cluster_arn = resource_id
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
        automation_output = ecs_stop_tasks(
          client=client,
          cluster_arn=cluster_arn,
          task=described_task
        )

        if 'error' in automation_output:
          return automation_output

  if automation_output == '':
    automation_output = "No Running Tasks, Exiting..."

  return automation_output

  
def info() -> dict:
  INFO = {
  "displayName": "Restart Privileged ECS Tasks",
  "description": "Restarts ECS Tasks that have Privileged Access Permissions",
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
