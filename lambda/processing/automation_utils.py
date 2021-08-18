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
    elif resource['type'] == 'SQS Queue':
        client = boto_session.client('sqs')
        client.tag_queue(
            QueueUrl=resource['attributes']['Queue URL'],
            Tags={
                key: value
            }
        )
    elif parse_arn(resource['arn'])['service'] == 'ec2':
        client = boto3.client('ec2')
        client.create_tags(
            Resources=[
                resource['id'],
            ],
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
                key,
            ]
        )
    elif parse_arn(resource['arn'])['service'] == 'ec2':
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
