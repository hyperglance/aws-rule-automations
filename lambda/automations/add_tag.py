"""Tags an EC2 Resource

This automation attempts to add a tag for a resource, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to Tag a resource

    Parameters
    ----------
    boto_session : object
      The boto session to use to invoke the automation
    resource: dict
      Dict of  Resource attributes touse in the automation
    automation_params : str
      Automation parameters passed from the Hyperglance UI
    """

    key = automation_params.get('Key')
    value = automation_params.get('Value')
    client = boto_session.client('ec2')  # remove this hardcoding when parsing of arn is implemented
    tags = resource['tags']

    if key in tags.keys():
        logger.error("tag " + key + "is already present - aborting automation")
        return

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

def info() -> dict:
    INFO = {
        "displayName": "Add Tag",
        "description": "Add a tag to a resource",
        "resourceTypes": [
            "Security Group",
            "EC2 Instance",
            "EC2 Image",
            "Internet Gateway",
            "Network Acl",
            "Network Interface",
            "Placement Group",
            "Route Table",
            "EC2 Snapshot",
            "Subnet",
            "EBS Volume",
            "VPC",
            "SNS",
            "SQS"
        ],
        "params": [
            {
                "name": "Key",
                "type": "string",
                "default": ""
            },
            {
                "name": "Value",
                "type": "string",
                "default": ""
            }
        ]
    }

    return INFO
