"""Tags an EC2 Resource

This automation attempts to fix a tag in for an EC2 resource, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
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
  dry_run = automation_params.get('DryRun').lower() in ['true', 'y', 'yes']

  client = boto_session.client('ec2')

  for old_key, value in resource['matchedAttributes'].items():
    # only interested in tags
    if old_key not in resource['tags']:
      continue

    # tag might already be 'good'
    if old_key == new_key:
      continue

  
    ## Create the new tag and retain existing value
    client.create_tags(
      Resources=[
        resource['id'],
      ],
      DryRun=dry_run,
      Tags=[
        {
          'Key': new_key,
          'Value': value
        },
      ]
    )
  
    ## Remove the old offending tag (we make sure to do the destructive action 2nd!)
    client.delete_tags(
      Resources=[
        resource['id'],
      ],
      DryRun=dry_run,
      Tags=[
        {
          'Key': old_key,
          'Value': value
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
      "VPC"
    ],
    "params": [
      {
        "name": "New Key",
        "type": "string",
        "default": ""
      },
      {
        "name": "DryRun",
        "type": "boolean",
        "default": "true"
      }
    ]
  }

  return INFO