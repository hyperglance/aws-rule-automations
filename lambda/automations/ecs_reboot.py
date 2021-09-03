"""ECS Reboot

This automation attempts to stop tasks in an ECS Cluster identified as above or below the configured threshold by Hyperglance Rule(s). Tasks started by ECS Services will be recreated and come back running if configured.

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
            client.stop_task(
                cluster=cluster_arn,
                task=task,
                reason='Privileged tasks are dangerous'
            )


def info() -> dict:
    INFO = {
        "displayName": "Restart Privileged ECS Tasks",
        "description": "Stops ECS Tasks that have Privileged Access Permissions. Tasks started by ECS Services will be recreated and come back running if configured.",
        "resourceTypes": [
            "ECS Cluster"
        ],
        "params": [
            {
                "name": "Role",
                "type": "string",
                "default": " "
            }
        ],
        "permissions": [
            "ecs:ListTasks",
            "ecs:DescribeTasks",
            "ecs:DescribeTaskDefinition",
            "ecs:StopTask"
        ]
    }
    return INFO
