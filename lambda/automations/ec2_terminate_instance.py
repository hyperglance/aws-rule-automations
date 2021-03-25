"""EC2 Terminate Instance

This automation Terminates an EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import os
import automations.ec2_snapshot_instance


## Stop EC2 Instance
def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Terminate an EC2 Instance

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

  client = boto_session.client('ec2')
  ec2_instance = resource_id

  if automation_params.get('SnapShotBeforeTerminate').lower() in ['true', 'y', 'yes']:
    ec2_snapshot_instance = ec2_snapshot_instance()
    response = ec2_snapshot_instance(
      boto_session, 
      resource_id
      )

    if response['ResponseMetadata']['HTTPStatusCOde'] >= 400:
      automation_output = "Something went wrong with the snapshot for instance {}, abandoning termination".format(ec2_instance)
      return automation_output
  else:
    response = client.terminate_instances(
      InstanceIds=[ec2_instance], 
      DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
      )

    result = response['ResponseMetadata']['HTTPStatusCode']
    if result >= 400:
      automation_output = "An unexpected error occured, error message: {}".format(result)
    else:
      automation_output = "Instance {} terminated".format(ec2_instance)

    return automation_output

  
def info() -> dict:
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