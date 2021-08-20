"""
This automation Quarantines and EC2 Instance, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to Qurantine and EC2 Instance

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
    ec2_resource = boto_session.resource('ec2')

    ec2_instance = resource['attributes']['Instance ID']
    vpc_id = resource['attributes']['VPC ID']

    ## Check if there already is a qurantine SG, if not, create one
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

    quarantine_sg_id = ''

    if response['SecurityGroups']:
        quarantine_sg_id = response['SecurityGroups'][0]['GroupId']
        logger.info("Already quarantined by security group: {}".format(quarantine_sg_id))
    else:
        response = client.create_security_group(
            Description='Quarantine Security Group. Created by Hyperglance automations. Do NOT attach Ingress or Egress rules.',
            GroupName='Quarantined_By_Hyperglance',
            VpcId=vpc_id
        )

        quarantine_sg_id = response['GroupId']

        ## Remove the default Security Groups Rules
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

    ## Finally attach the instance to SG
    ec2_resource.Instance(ec2_instance).modify_attribute(Groups=[quarantine_sg_id])


def info() -> dict:
    INFO = {
        "displayName": "Quarantine EC2 Instance",
        "description": "Quarantines and EC2 Instance by attaching it to a Security group with no Ingress or Egress rules",
        "resourceTypes": [
            "EC2 Instance"
        ],
        "params": [

        ],
        "permissions": [
            "ec2:DescribeSecurityGroups",
            "ec2:CreateSecurityGroup",
            "ec2:RevokeSecurityGroupEgress",
            "ec2:ModifyInstanceAttribute"
        ]
    }

    return INFO
