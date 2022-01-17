"""EC2 Delete NAT Gateway

This automation Deletes a NAT Gateway, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete a NAT Gateway

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
  gateway_id = resource['attributes']['NAT Gateway ID']

  client.delete_nat_gateway(
    NatGatewayId=gateway_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete NAT Gateway",
    "description": "Deletes a specified NAT Gateway",
    "resourceTypes": [
      "NAT Gateway"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "boolean",
        "default": "true"
      }
    ],
    "permissions": [
      "ec2:DeleteNatGateway"
    ]
  }

  return INFO