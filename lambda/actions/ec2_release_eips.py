"""EC2 Release Elastic IPs

This action Release Instanc Elastic IPs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ]) -> str:
  """ Attempts to release EIPs

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on
  table : list
    A list of additional resource values that may be required

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  ec2_instance = resource_id

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
      eip_association_id = ec2_eip['AssociationId']
      response = client.disassociate_address(
        AssociationId=eip_association_id
      )

      result = response['ResponseMetadata']['HTTPStatusCode']
      if result >= 400:
        action_output = "An unexpected error occured, error message: {}".format(result)
        return action_output
      else:
        action_output += "Disassociated EIP: {}".format(ec2_eip['PublicIp'])

      eip_allocation_id = ec2_eip['AllocationId']
      response = client.release_address(
        AllocationId=eip_allocation_id
      )

      result = response['ResponseMetadata']['HTTPStatusCode']
      if result >= 400:
        action_output = "An unexpected error occured, error message: {}".format(result)
      else:
        action_output += "Released EIP: {}".format(ec2_eip['PublicIp'])
  else:
    action_output = "No EIPs found, please check rule configuration"

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Release Elastic IP",
    "description": "Releases and Elastic IP from associated EC2 Instance",
    "resourceTypes": [
      "EC2 Instance",
      "Elatic IP Address"
    ],
    "params": [

    ]
  }

  return INFO