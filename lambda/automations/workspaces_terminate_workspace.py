"""Workspaces - Terminate Workspace

This automation Terminates a Workspace, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Terminate a Workspace

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

  client.terminate_workspaces(
    TerminateWorkspaceRequests=[
      {
        'WorkspaceId': workspace_id
      },
    ]
  )


def info() -> dict:
  INFO = {
    "displayName": "Terminate Workspace",
    "description": "Terminates a Running Workspacee",
    "resourceTypes": [
      "Workspace"
    ],
    "params": [

    ],
    "permissions": [
      "workspaces:TerminateWorkspaces"
    ]
  }

  return INFO

  