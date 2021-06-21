"""EC2 Delete Internet Gateway

This automation Deletes and Internet Gateway, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete and Internet Gateway

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """
  client = boto_session.client('ec2')
  gateway_id = resource['attributes']['Internet Gateway ID']

  client.delete_internet_gateway(
    InternetGatewayId=gateway_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete Internet Gateway",
    "description": "Deletes a specified Internet Gateway",
    "resourceTypes": [
      "Internet Gateway"
    ],
    "params": [

    ]
  }

  return INFO