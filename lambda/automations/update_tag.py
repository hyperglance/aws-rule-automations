"""Tags an EC2 Resource

This automation attempts to update a tag key for a resource, identified as above or below the configured threshold
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

    new_key = automation_params.get('New Key')
    old_key = automation_params.get('Old Key')
    client = boto_session.client('ec2')  # remove this hardcoding when parsing of arn is implemented
    tags = resource['tags']

    if new_key in tags.keys():
        logger.error("tag " + new_key + "is already present - aborting automation")
        return
    elif not old_key in tags.keys():
        logger.error("tag " + old_key + "is not present - aborting automation")
        return

    client.create_tags(
        Resources=[
            resource['id'],
        ],
        Tags=[
            {
                'Key': new_key,
                'Value': tags[old_key]
            },
        ]
    )

    ## Remove the old offending tag (we make sure to do the destructive action 2nd!)
    client.delete_tags(
        Resources=[
            resource['id'],
        ],
        Tags=[
            {
                'Key': old_key,
                'Value': tags[old_key]
            },
        ]
    )


def info() -> dict:
    INFO = {
        "displayName": "Replace Tag",
        "description": "Replaces a tag's key but keeps its value",
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
                "name": "New Key",
                "type": "string",
                "default": ""
            },
            {
                "name": "Old Key",
                "type": "string",
                "default": ""
            }
        ]
    }

    return INFO
