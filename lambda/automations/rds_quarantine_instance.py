"""RDS Aurora Quarantine Instance

This automation Quarantines and Aurora RDS Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to set Quarantine an RDS Aurora Instance

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

  ## Requires multiple clients to handle all automation components
  ec2_resource = boto_session.resource('ec2')
  ec2_client = boto_session.client('ec2')
  rds_client = boto_session.client('rds')

  rds_db = resource_id
  vpc_id = table[0]['VPC ID']

  ## Check if there is a qurantine SG, if not, create one

  try:
    response = ec2_client.describe_security_groups(
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
      automation_output = "Founc existing qurantine security group: {}".format(hyperglance_quarantine_sg)
    else:
      response = ec2_client.create_security_group(
        Description='Quarantine Security Group. Created by Hyperglance automations. Do NOT attach Ingress or Egress rules.',
        GroupName='Quarantined_By_Hyperglance',
        VpcId=vpc_id
      )

      ## Remove default security group rules
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
    automation_output = "An unexpected client error has occured: {}".format(err)

  automation_output += "Quaranting Instance: {} SGs, blocking Ingress and Egress".format(rds_db)

  ## Finally attach the RDS Instance to the Quarantine SG

  try:
    response = rds_client.modify_db_instance(
      DBInstanceIdentifier=rds_db,
      VpcSecurityroupIds=[hyperglance_quarantine_sg],
      ApplyImmediately=True
    )

    result = response['ResponseMetadata']['HTTPStatusCode']
    if result >= 400:
      automation_output += "An unexpected error occured attaching the quarantine security group: {}".format(result)
    else:
      automation_output += "Attached Quarantine Security Group to RDS Instance: {}".format(rds_db)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Quarantine RDS Instance",
    "description": "Quarantines and RDS Instance by applying a DENY ALL Security Group",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO