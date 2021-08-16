"""EC2 Release Elastic IPs

This automation Release Instanc Elastic IPs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import logging

logger = logging.getLogger()

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to release EIPs

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
  ec2_instance = resource['attributes']['Instance ID']

  describe_ec2_addresses = client.describe_addresses(
    Filters=[
      {
        'Name': 'instance-id',
        'Values': [ec2_instance]
      }
    ]
  )

  ec2_eip_addresses = describe_ec2_addresses['Addresses']

  if ec2_eip_addresses:
    for ec2_eip in ec2_eip_addresses:
     
      client.disassociate_address(
        AssociationId=ec2_eip['AssociationId']
      )
      logger.debug( "Disassociated EIP: {}".format(ec2_eip['PublicIp']))

      client.release_address(
        AllocationId=ec2_eip['AllocationId']
      )
      logger.debug("Released EIP: {}".format(ec2_eip['PublicIp']))
  else:
    logger.debug("No EIPs found")


def info() -> dict:
  INFO = {
    "displayName": "Release Elastic IP",
    "description": "Releases and Elastic IP from associated EC2 Instance",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ],
    "permissions": [

    ]
  }

  return INFO