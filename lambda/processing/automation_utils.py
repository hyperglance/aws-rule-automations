"""
Miscellaneous resources to help with processing Hyperglance automations
"""
import boto3


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
    match resource['type']:
        case 'SNS Topic':
            client = boto_session.client('sns')
            client.tag_resource(
                ResourceArn=resource['arn'],
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'SQS Queue':
            client = boto_session.client('sqs')
            response = client.tag_queue(
                QueueUrl=resource['attributes']['Queue URL'],
                Tags={
                    key: value
                }
            )
        case 'VPC':
            ec2 = boto_session.resource('ec2')
            vpc = ec2.Vpc(resource['id'])
            tag = vpc.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'Subnet':
            ec2 = boto3.resource('ec2')
            subnet = ec2.Subnet(resource['id'])
            tag = subnet.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'EC2 Snapshot':
            ec2 = boto3.resource('ec2')
            snapshot = ec2.Snapshot(resource['id'])
            tag = snapshot.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'Route Table': #this will not work -> no API methods it seems
            ec2 = boto3.resource('ec2')
            route_table = ec2.RouteTable(resource[id])
            tag = route_table.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        #case 'EBS Volume': no API methods it seems
        #case 'Placement Group': no API methods...
        case 'Network Interface':
            ec2 = boto3.resource('ec2')
            network_interface = ec2.NetworkInterface(resource['id'])
            tag = network_interface.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'Network ACL':
            ec2 = boto3.resource('ec2')
            network_acl = ec2.NetworkAcl(resource['id'])
            tag = network_acl.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'Internet Gateway':
            ec2 = boto3.resource('ec2')
            internet_gateway = ec2.InternetGateway(resource['id'])
            tag = internet_gateway.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'EC2 Image':
            ec2 = boto3.resource('ec2')
            image = ec2.Image(resource['id'])
            tag = image.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'EC2 Instance':
            ec2 = boto3.resource('ec2')
            instance = ec2.Instance(resource[id])
            tag = instance.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )
        case 'Security Group':
            ec2 = boto3.resource('ec2')
            security_group = ec2.SecurityGroup(resource['id'])
            tag = security_group.create_tags(
                Tags=[
                    {
                        'Key': key,
                        'Value': value
                    },
                ]
            )

def remove_tag(boto_session, key, resource):
    match resource['type']:
        case 'SNS Topic':
            client = boto3.client('sns')
            response = client.untag_resource(
                ResourceArn=resource['arn'],
                TagKeys=[
                    key,
                ]
            )
        case 'SQS Queue':
            client = boto_session.client('sqs')
            response = client.untag_queue(
                QueueUrl=resource['attributes']['Queue URL'],
                TagKeys=[
                    'string',
                ]
            )
        case 'VPC':
            client = boto_session.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    }
                ]
            )
        case 'Subnet': #this will not work
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    }
                ]
            )
        case 'EC2 Snapshot':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    }
                ]
            )
        case 'Route Table':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )
        #case 'ebs': no API calls
        #case 'placement groups'  no api calls
        case 'Network Interface':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )
        case 'Network Acl':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )
        case 'Internet Gateway':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )
        case 'EC2 Image':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )
        case 'EC2 Instance':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )
        case 'Security Group':
            client = boto3.client('ec2')
            response = client.delete_tags(
                Resources=[
                    resource['id'],
                ],
                Tags=[
                    {
                        'Key': key
                    },
                ]
            )



