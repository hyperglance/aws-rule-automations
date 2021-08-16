"""Detach External Layers from Lambda Function

This automation detaches external layers from a lambda function, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to remove external layers from a Lambda

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('lambda')

  account_id = resource['account']
  lambda_function = resource['attributes']['Function Name']


  lambda_layers = client.get_function(
    FunctionName=lambda_function
  )['Configuration'].get('Layers', [])

  ## Remove layers....
  new_lambda_layers = [layer.get('Arn') for layer in lambda_layers if account_id not in layer['Arn']]

  if len(lambda_layers) != len(new_lambda_layers):
    client.update_function_configuration(
      FunctionName=lambda_function,
      Layers=new_lambda_layers
    )


def info() -> dict:
  INFO = {
    "displayName": "Remove Layers",
    "description": "Removes Layers from a Lambda Function.",
    "resourceTypes": [
      "Lambda Function"
    ],
    "params": [

    ],
    "permissions": [
      "lambda:GetFunction",
      "lambda:UpdateFunctionConfiguration"
    ]
  }

  return INFO