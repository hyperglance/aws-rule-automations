"""Workspaces - Terminate Workspace

This automation Terminates a Workspace, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Terminate a Workspace

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
  client = boto_session.client('workspaces')
  workspace_id = resource_id

  try:
    response = client.terminate_workspaces(
      TerminateWorkspaceRequests=[
        {
          'WorkspaceId': workspace_id
        },
      ]
    )
    automation_output = "Terminated Workspace ID: {}".format(workspace_id)

  except ClientError as err:
    automation_output = "An unexpected error occured, error message {}".format(err)
    
  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Terminate Workspace",
    "description": "Terminates a Running Workspacee",
    "resourceTypes": [
      "Workspace"
    ],
    "params": [

    ]
  }

  return INFO

  