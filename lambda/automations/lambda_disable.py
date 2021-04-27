"""
This automation disables a lambda function, and sets it to latest version, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to disable a lambda function

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
  client = boto_session.client('lambda')
  lambda_funciton = resource['attributes']['Function Name']

  try:
    response = client.put_function_concurrency(
      FunctionName=lambda_funciton,
      ReservedConcurrentExecutions=0
    )
    automation_output = "Lambda function: {} successfully disabled".format(lambda_funciton)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Disable Lambda",
    "description": "Disables a Lambda from Executing",
    "resourceTypes": [
      "Lambda Function"
    ],
    "params": [

    ]
  }

  return INFO