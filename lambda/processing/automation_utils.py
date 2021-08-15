"""
Miscellaneous resources to help with processing Hyperglance automations
"""
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_arn(arn) -> dict:
    """

    Parameters
    ----------
    The arn string in the form of

    arn:partition:service:region:account-id:resource-id
    arn:partition:service:region:account-id:resource-type/resource-id
    arn:partition:service:region:account-id:resource-type:resource-id

    Returns
    -------
    A dict containing the separate elements
    """

    elements = arn.split(':', 5)
    result = {
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_type': None
    }
    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/', 1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':', 1)
    return result


def add_tag(boto_session, key, value, resource):
    if resource['type'] == 'SNS Topic':
        logger.info('SNS ADD TAG')
        logger.info(resource)
        client = boto_session.client('sns')
        response = client.tag_resource(
            ResourceArn=resource['arn'],
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
        logger.info(response)
    elif resource['type'] == 'SQS Queue':
        client = boto_session.client('sqs')
        client.tag_queue(
            QueueUrl=resource['attributes']['Queue URL'],
            Tags={
                key: value
            }
        )
    elif resource['type'] == 'VPC':
        ec2 = boto_session.resource('ec2')
        vpc = ec2.Vpc(resource['id'])
        vpc.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'Subnet':
        ec2 = boto3.resource('ec2')
        subnet = ec2.Subnet(resource['id'])
        subnet.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )

    elif resource['type'] == 'EC2 Snapshot':
        ec2 = boto3.resource('ec2')
        snapshot = ec2.Snapshot(resource['id'])
        snapshot.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'Route Table':
        ec2 = boto3.resource('ec2')
        route_table = ec2.RouteTable(resource['id'])
        route_table.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    # case 'EBS Volume': no API methods it seems
    # case 'Placement Group': no API methods...
    elif resource['type'] == 'Network Interface':
        ec2 = boto3.resource('ec2')
        network_interface = ec2.NetworkInterface(resource['id'])
        network_interface.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'Network ACL':
        ec2 = boto3.resource('ec2')
        network_acl = ec2.NetworkAcl(resource['id'])
        network_acl.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'Internet Gateway':
        ec2 = boto3.resource('ec2')
        internet_gateway = ec2.InternetGateway(resource['id'])
        internet_gateway.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'EC2 Image':
        ec2 = boto3.resource('ec2')
        image = ec2.Image(resource['id'])
        image.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'EC2 Instance':
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(resource['id'])
        instance.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
    elif resource['type'] == 'Security Group':
        ec2 = boto3.resource('ec2')
        security_group = ec2.SecurityGroup(resource['id'])
        security_group.create_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )


def remove_tag(boto_session, key, resource):
    if resource['type'] == 'SNS Topic':
        client = boto3.client('sns')
        response = client.untag_resource(
            ResourceArn=resource['arn'],
            TagKeys=[
                key,
            ]
        )
    elif resource['type'] == 'SQS Queue':
        client = boto_session.client('sqs')
        client.untag_queue(
            QueueUrl=resource['attributes']['Queue URL'],
            TagKeys=[
                'string',
            ]
        )
    elif resource['type'] == 'VPC'\
            or resource['type'] == 'Subnet'\
            or resource['type'] == 'EC2 Snapshot'\
            or resource['type'] == 'Route Table'\
            or resource['type'] == 'Network Interface'\
            or resource['type'] == 'Network ACL'\
            or resource['type'] == 'Internet Gateway'\
            or resource['type'] == 'EC2 Image'\
            or resource['type'] == 'EC2 Instance'\
            or resource['type'] == 'Security Group':
        client = boto_session.client('ec2')
        client.delete_tags(
            Resources=[
                resource['id'],
            ],
            Tags=[
                {
                    'Key': key
                }
            ]
        )

