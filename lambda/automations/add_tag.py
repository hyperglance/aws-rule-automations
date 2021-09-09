"""Tags an EC2 Resource

This automation attempts to add a tag for a resource, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""
import logging
import processing.automation_utils as utils

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
    tags = resource['tags']

    if key in tags.keys():
        logger.error("tag " + key + "is already present - aborting automation")
        return
    utils.add_tag(boto_session, key, value, resource)

def info() -> dict:
    INFO = {
        "displayName": "Add Tag",
        "description": "Adds a tag to a resource",
        "resourceTypes": [
            "Security Group",
            "EC2 Instance",
            "AMI",
            "Internet Gateway",
            "Network Acl",
            "Network Interface",
            "Route Table",
            "EBS Snapshot",
            "EBS Volume",
            "Subnet",
            "VPC",
            "SNS Topic",
            "SQS Queue"
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
        ],
        "permissions": [
            "ec2:CreateTags",
            "sns:TagResource",
            "sqs:TagQueue",
            "sqs:GetQueueUrl"
        ]
    }

    return INFO
