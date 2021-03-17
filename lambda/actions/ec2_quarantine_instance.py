"""
This action Quarantines and EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ], action_params = '') -> str:
  """ Attempts to Qurantine and EC2 Instance

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
  ec2_resource = boto_session.resource('ec2')

  ec2_instance = resource_id
  vpc_id = table[0]['VPC ID']

  ## Check if there already is a qurantine SG, if not, create one

  try:
    response = client.describe_security_groups(
      Filters=[
        {
          'Name': 'group-name',
          'Values': ['Quarantined_By_Hyperglance']
        },
        {
          'Name': 'vpc-id',
          'Values': [vpc_id]
        }
      ]
    )

    if response['SecurityGroups']:
      hyperglance_quarantine_sg = response['SecurityGroups'][0]['GroupId']
      action_output = "Found existing qurantine security group: {}".format(hyperglance_quarantine_sg)
    else:
      response = client.create_security_group(
        Description='Quarantine Security Group. Created by Hyperglance Actions. Do NOT attach Ingress or Egress rules.',
        GroupName='Quarantined_By_Hyperglance',
        VpcId=vpc_id
      )

      ## Remove the default Security Groups Rules
      created_security_group = ec2_resource.SecurityGroup(response['GroupId'])
      delete_response = created_security_group.revoke_egress(
        GroupId=response['GroupId'],
        IpPermissions=[
          {
            'IpProtocol': '-1',
            'IpRanges': [
              {
                'CidrIp': '0.0.0.0/0'
              }
            ]
          }
        ]
      )

  except ClientError as err:
    action_output = "An unexpected client error has occured: {}".format(err)

  action_output += "Quarantining Instance: {} - Updating SG attachments".format(ec2_instance)

  ## Finally attach the instance to Qurantine SG

  try:
    response = ec2_resource.Instance(ec2_instance).modify_attribute(Groups=[hyperglance_quarantine_sg])
    
    result = response['ResponseMetadata']['HTTPStatusCode']
    if result >= 400:
      action_output += "An unexpected error occured attaching the quarantine secuity group: {}".format(result)
    else:
      action_output += "Attached Qurantine Security Group to instance: {}".format(ec2_instance)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Quarantine EC2 Instance",
    "description": "Quarantines and EC2 Instance by attaching it to a Security group with no Ingress or Egress rules",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO