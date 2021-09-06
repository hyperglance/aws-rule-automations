"""ECS Stop

This automation attempts to stop running tasks in an ECS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to reboot running ecs tasks

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

    client = boto_session.client('ecs')

    cluster_arn = resource['arn']
    role_arn = automation_params.get('Role')

    # Get a list of running tasks for the cluster
    running_tasks = client.list_tasks(
        cluster=cluster_arn,
        desiredStatus='RUNNING'
    )['taskArns']

    for task in running_tasks:

        client.stop_task(
            cluster=cluster_arn,
            task=task

        )


def info() -> dict:
    INFO = {
        "displayName": "Stop ECS Cluster",
        "description": "Stops ECS Cluster",
        "resourceTypes": [
            "ECS Cluster"
        ],
        "params": [

        ],
        "permissions": [
            "ecs:ListTasks",
            "ecs:DescribeTasks",
            "ecs:DescribeTaskDefinition",
            "ecs:StopTask",
            "ecs:UpdateContainerInstancesState"
        ]
    }

    return INFO
