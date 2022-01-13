"""Detach External Layers from Lambda Function

This automation detaches external layers from a lambda function, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import logging


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

  response = client.update_function_configuration(
    FunctionName=lambda_function,
    Layers=[]
  )



def info() -> dict:
  INFO = {
    "displayName": "Remove Layers",
    "description": "Removes layers from a Lambda Function",
    "resourceTypes": [
      "Lambda Function"
    ],
    "params": [

    ],
    "permissions": [
      "lambda:GetFunction",
      "lambda:UpdateFunctionConfiguration",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
  }

  return INFO