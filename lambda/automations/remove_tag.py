"""

This automation attempts to remove a tag for a resource, identified as above or below the configured threshold
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
    client = boto_session.client('ec2')  # remove this hardcoding when parsing of arn is implemented
    tags = resource['tags']

    if not key in tags.keys():
        logger.error(tags)
        logger.error("tag " + key + " is not present - aborting automation")
        return


    client.delete_tags(
        Resources=[
            resource['id'],
        ],
        Tags=[
            {
                'Key': key,
                'Value': tags[key]
            },
        ]
    )


def info() -> dict:
    INFO = {
        "displayName": "Replace Tag",
        "description": "Replaces a tag's key but keeps its value (EC2 only)",
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
            "SQS",
            "SNS"
        ],
        "params": [
            {
                "name": "Key",
                "type": "string",
                "default": ""
            }
        ]
    }

    return INFO
