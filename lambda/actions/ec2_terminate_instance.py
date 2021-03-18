"""EC2 Terminate Instance

This action Terminates an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

import os
import actions.ec2_snapshot_instance


## Stop EC2 Instance
def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Terminate an EC2 Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  ec2_instance = resource_id

  if os.getenv("SnapShotBeforeTerminate", 'False').lower() in ['true', '1', 'y', 'yes']:
    ec2_snapshot_instance = ec2_snapshot_instance()
    response = ec2_snapshot_instance(
      boto_session, 
      rule
      )

    if response['ResponseMetadata']['HTTPStatusCOde'] >= 400:
      action_output = "Something went wrong with the snapshot for instance {}, abandoning termination".format(ec2_instance)
      return action_output
  else:
    response = client.terminate_instances(
      InstanceIds=[ec2_instance], 
      DryRun=os.getenv("DryRun", 'False').lower() in ['true', '1', 'y', 'yes']
      )

    result = response['ResponseMetadata']['HTTPStatusCode']
    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "Instance {} terminated".format(ec2_instance)

    return action_output

  
def info() -> str:
  INFO = {
    "displayName": "Terminate Instance",
    "description": "Terminates EC2 Instance",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "bool",
        "default": "True"
      }
    ]
  }

  return INFO