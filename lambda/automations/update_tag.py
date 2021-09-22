"""Tags an EC2 Resource

This automation attempts to fix a tag in for an EC2 resource, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

import processing.automation_utils as utils


def hyperglance_automation(boto_session, resource: dict, automation_params=''):
    """ Attempts to Tag an EC2 Resource

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

    matched_tag_attrs = [attr for attr in resource['matchedAttributes'].items() if attr[0] in resource['tags']]

    if (len(matched_tag_attrs) == 0):
        res_id = resource['id']
        raise RuntimeError(f'No tags to update on {res_id} because none of its tags matched the search criteria.')

    for old_key, value in matched_tag_attrs:
        # tag might already be 'good'
        if old_key == new_key:
            continue

        ## Create the new tag and retain existing value
        utils.add_tag(boto_session, new_key, value, resource)

        ## Remove the old offending tag (we make sure to do the destructive action 2nd!)
        utils.remove_tag(boto_session, old_key, resource)


def info() -> dict:
    INFO = {
        "displayName": "Update Tag",
        "description": "Replaces a tags key but keeps its value",
        "resourceTypes": [
            "Security Group",
            "EC2 Instance",
            "AMI",
            "Internet Gateway",
            "Network ACL",
            "Network Interface",
            "Placement Group",
            "Route Table",
            "EC2 Snapshot",
            "Subnet",
            "EBS Snapshot",
            "EBS Volume",
            "VPC",
            "SNS Topic",
            "SQS Queue"
        ],
        "params": [
            {
                "name": "New Key",
                "type": "string",
                "default": ""
            }
        ],
        "permissions": [
            "ec2:CreateTags",
            "sns:TagResource",
            "sqs:TagQueue",
            "ec2:DeleteTags",
            "sns:UntagResource",
            "sqs:UntagQueue"
        ]
    }

    return INFO
