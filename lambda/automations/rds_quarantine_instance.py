"""RDS Aurora Quarantine Instance

This automation Quarantines and Aurora RDS Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to set Quarantine an RDS Aurora Instance

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  ## Requires multiple clients to handle all automation components
  ec2_resource = boto_session.resource('ec2')
  ec2_client = boto_session.client('ec2')
  rds_client = boto_session.client('rds')

  rds_db = resource['id']
  vpc_id = resource['attributes']['VPC ID']

  ## Check if there is a qurantine SG, if not, create one

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
  else:
    response = ec2_client.create_security_group(
      Description='Quarantine Security Group. Created by Hyperglance automations. Do NOT attach Ingress or Egress rules.',
      GroupName='Quarantined_By_Hyperglance',
      VpcId=vpc_id
    )

    ## Remove default security group rules
    created_security_group = ec2_resource.SecurityGroup(response['GroupId'])
    created_security_group.revoke_egress(
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

    hyperglance_quarantine_sg = response['GroupId']



  ## Finally attach the RDS Instance to the Quarantine SG

  rds_client.modify_db_instance(
    DBInstanceIdentifier=rds_db,
    VpcSecurityGroupIds=[hyperglance_quarantine_sg],
    ApplyImmediately=True
  )


def info() -> dict:
  INFO = {
    "displayName": "Quarantine RDS Instance",
    "description": "Quarantines and RDS Instance by applying a DENY ALL Security Group",
    "resourceTypes": [
      "RDS DB Instance"
    ],
    "params": [

    ],
    "permissions": [
      "ec2:DescribeSecurityGroups",
      "ec2:CreateSecurityGroup",
      "ec2RevokeSecurityGroupEgress",
      "rds:ModifyDBInstance"
    ]
  }

  return INFO