## workspaces_terminate_workspace.py

## Deletes Worspace identified by the configured Hyperglance Rule
import boto3
from botocore.exceptions import ClientError

## Terminate Workspace
def hyperglance_action(boto_session, rule, entity, params):
  client = boto_session.client('workspaces')
  workspace_id = entity['id']

  try:
    response = client.terminate_workspaces(
      WorkspaceId=workspace_id
    )
    action_output = "Terminated Workspace ID: {}".format(workspace_id)

  except ClientError as err:
    action_output = "An unexpected error occured, error message {}".format(err)
    
  return action_output


