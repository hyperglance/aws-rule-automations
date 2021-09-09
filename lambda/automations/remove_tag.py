"""

This automation attempts to remove a tag for a resource, identified as above or below the configured threshold
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
    tags = resource['tags']

    if not key in tags.keys():
        logger.error(tags)
        logger.error("tag " + key + " is not present - aborting automation")
        return

    utils.remove_tag(boto_session, key, resource)



def info() -> dict:
    INFO = {
        "displayName": "Remove Tag",
        "description": "Removes a tag",
        "resourceTypes": [
            "Security Group",
            "EC2 Instance",
            "AMI",
            "Internet Gateway",
            "Network Acl",
            "Network Interface",
            "Route Table",
            "EBS Snapshot",
            "EBS Volume"
            "Subnet",
            "VPC",
            "SQS Queue",
            "SNS Topic"
        ],
        "params": [
            {
                "name": "Key",
                "type": "string",
                "default": ""
            }
        ],
        "permissions": [
            "ec2:DeleteTags",
            "sns:UntagResource",
            "sqs:UntagQueue"
        ]
    }

    return INFO
