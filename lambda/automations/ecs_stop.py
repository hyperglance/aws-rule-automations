"""ECS Stop

This automation attempts to stop running tasks in an ECS Cluster, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to stop running ecs tasks

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
    drain_ec2instance = automation_params.get('DrainEC2Instance')

    ## Get a list of running tasks for the cluster
    running_tasks = client.list_tasks(
        cluster=cluster_arn,
        desiredStatus='RUNNING'
    )['taskArns']

    for task in running_tasks:
        described_task = client.describe_tasks(
            cluster=cluster_arn,
            tasks=[task, ]
        )['tasks'][0]

        task_definition = described_task.get('taskDefinitionArn')

        definition = client.describe_task_definition(
            taskDefinition=task_definition
        )['taskDefinition']

        if definition.get('executionRoleArn') == role_arn:
            if 'EC2' in described_task.get('launchType') and drain_ec2instance:
                client.update_container_instance_state(
                    cluster=cluster_arn,
                    containerInstances=[described_task.get('containerInstanceArn')],
                    status='DRAINING'
                )

            client.stop_task(
                cluster=cluster_arn,
                task=task,
                reason='Stop task triggered by automation rule'
            )


def info() -> dict:
    INFO = {
        "displayName": "Stop ECS Cluster",
        "description": "Stops ECS Tasks with the given Role parameter. Tasks started by ECS Services will be recreated and come back running if configured. Passing true for the DrainEC2Instance parameter will drain the instance and prevent it from recreating the tasks.",
        "resourceTypes": [
            "ECS Cluster"
        ],
        "params": [
            {
                "name": "Role",
                "type": "string",
                "default": " "
            },
            {
                "name": "DrainEC2Instance",
                "type": "boolean",
                "default": "false"
            }
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
