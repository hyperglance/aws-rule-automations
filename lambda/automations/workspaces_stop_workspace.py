"""Workspaces - Stop Workspace

This automation Stops a Workspace, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Stop and Workspace

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('workspaces')
  workspace_id = resource['id']

  client.stop_workspaces(
    StopWorkspaceRequests=[
      {
        'WorkspaceId': workspace_id
      },
    ]
  )


def info() -> dict:
  INFO = {
    "displayName": "Stop Workspace",
    "description": "Stops a Workspace",
    "resourceTypes": [
      "Workspace"
    ],
    "params": [

    ],
    "permissions": [
      "workspaces:StopWorkspaces"
    ]
  }

  return INFO
  