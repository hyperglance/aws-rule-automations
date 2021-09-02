"""
This automation Quarantines a VPC, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import json
import logging
from processing import automation_utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def attach_policy_to_all_users(client, policy_arn: str):
    ## Attach policy to each user
    account_users = client.list_users()['Users']
    for user in account_users:
        client.attach_user_policy(
            UserName=user.get('UserName'),
            PolicyArn=policy_arn
        )


def create_deny_policy(client, region: str, vpc_id: str):
    """ Attempts to Create a Deny all policy on EC2 and Security Group resources that are within the given VPC

  Parameters
  ----------
  client : object
    The boto client to use to invoke the automation
  region : str
    Target VPC Region
  vpc_id: str
    ID of the target VPC
  """
    ## Policy Definition
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "ec2:*",
                "Effect": "Deny",
                "Resource": [
                    automation_utils.generate_arn('ec2', vpc_id, 'aws', '*', region, '/', 'vpc'),
                    automation_utils.generate_arn('ec2', '*', 'aws', '*', region, '/', 'security-group')
                ],
                "Condition": {
                    "ForAnyValue:ArnEquals": {
                        "ec2:Vpc": automation_utils.generate_arn('ec2', vpc_id, 'aws', '*', region, '/', 'vpc')
                    }
                }
            }
        ]
    }

    ## Create the policy
    client.create_policy(
        PolicyName="isolate_{}_access_policy".format(vpc_id),
        PolicyDocument=json.dumps(policy)
    )



def create_isolation_acl(client, vpc_id: str):
    acls = client.describe_network_acls(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc_id
                ]
            },
        ],
    )

    ## Iterate through each ACL
    vpc_subnet_associations = []
    for acl in acls.get('NetworkAcls'):
        associations = acl.get('Associations', [])
        vpc_subnet_associations += [association.get('NetworkAclAssociationId') for association in associations]

    if vpc_subnet_associations:
        ## Create ACL with Deny ALL
        network_acl = client.create_network_acl(
            VpcId=vpc_id
        )

        for subnet_id in vpc_subnet_associations:
            if subnet_id:
                client.replace_network_acl_association(
                    AssociationId=subnet_id,
                    NetworkAclId=network_acl['NetworkAcl']['NetworkAclId']
                )


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to Quarantine a VPC

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

    ec2_client = boto_session.client('ec2')
    iam_client = boto_session.client('iam')

    vpc_id = resource['attributes']['VPC ID']
    region = resource['region']
    account = resource['account']
    policy_arn = automation_utils.generate_arn(
        'iam',
        f'isolate_{vpc_id}_access_policy',
        'aws',
        account,
        '',
        '/',
        'policy'
    )


    ## Disable DNS
    ec2_client.modify_vpc_attribute(
        EnableDnsSupport={
            'Value': False
        },
        VpcId=vpc_id
    )

    ## Create a Deny ACL
    create_isolation_acl(ec2_client, vpc_id)

    try:
        create_deny_policy(
            client=iam_client,
            region=region,
            vpc_id=vpc_id
        )
    except:
        pass  # Policy might already exist

    attach_policy_to_all_users(
        client=iam_client,
        policy_arn=policy_arn
    )

def info() -> dict:
    INFO = {
        "displayName": "Isolate VPC",
        "description": "Isolates an Entire VPC by applying a Deny ALL Network ACL and attaching a Deny All IAM Policy to all users",
        "resourceTypes": [
            "VPC"
        ],
        "params": [

        ],
        "permissions": [
            "ec2:ModifyVpcAttribute",
            "iam:CreatePolicy",
            "ec2:DescribeNetworkAcls",
            "ec2:CreateNetworkAcl",
            "ec2:ReplaceNetworkAclAssociation",
            "iam:ListUsers"
        ]
    }

    return INFO
