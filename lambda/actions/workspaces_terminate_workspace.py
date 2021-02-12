"""Workspaces - Terminate Workspace

This action Terminates a Workspace, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import boto3
from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to Terminate a Workspace

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on

  Returns
  -------
  string
    A string containing the status of the request

  """
  client = boto_session.client('workspaces')
  workspace_id = resource_id

  try:
    response = client.terminate_workspaces(
      WorkspaceId=workspace_id
    )
    action_output = "Terminated Workspace ID: {}".format(workspace_id)

  except ClientError as err:
    action_output = "An unexpected error occured, error message {}".format(err)
    
  return action_output

  