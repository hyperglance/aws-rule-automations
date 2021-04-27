"""Workspaces - Start Workspace

This automation Starts a Workspace, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to Start a Workspace

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

  client = boto_session.client('workspaces')
  workspace_id = resource['id']

  try:
    response = client.start_workspaces(
      StartWorkspaceRequests=[
        {
        'WorkspaceId': workspace_id
        },
      ]
    )
    automation_output = "Started Workspace ID: {}".format(workspace_id)

  except ClientError as err:
    automation_output = "An unexpected error occured, error message: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Start Workspace",
    "description": "Starts a Workspacee",
    "resourceTypes": [
      "Workspace"
    ],
    "params": [

    ]
  }

  return INFO