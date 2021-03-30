"""Detach External Layers from Lambda Function

This automation detaches external layers from a lambda function, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError


def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to remove external layers from a Lambda

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

  client = boto_session.client('lambda')

  lambda_function = resource_id

  try:
    lambda_layers = client.get_function(
      FunctionName=lambda_function
    )['Configuration']['Layers']
  except KeyError:
    return "The lambda function: {} has no layers".format(lambda_function)
  except ClientError as err:
    return "An unexpected Client error has occured, when getting layers, error: {}".format(err)

  ## Remove layers....
  for layer in lambda_layers:
    lambda_layers.remove(layer)

  new_lambda_layers = [layers.get('Arn') for layers in lambda_layers]

  ## Update the Lambda
  try:
    client.update_function_configuration(
      FunctionName=lambda_function,
      Layers=new_lambda_layers
    )
    automation_output = "Sucessfully removed layers from lambda: {}".format(lambda_function)

  except ClientError as err:
    automation_output = "An unexpect client error has occured, error: {}".format(err)
  
  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Remove Layers",
    "description": "Removes Layers from a Lambda Function.",
    "resourceTypes": [
      "Lambda"
    ],
    "params": [

    ]
  }

  return INFO