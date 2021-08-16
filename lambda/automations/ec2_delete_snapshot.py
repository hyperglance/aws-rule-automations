"""EC2 Delete Snapshot

This automation Deletes and EC2 Snapshot, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete and EC2 Snapshot

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('ec2')
  snapshot_id = resource['attributes']['Snapshot ID']

  client.delete_snapshot(
    SnapshotId=snapshot_id,
    DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete EBS Snapshot",
    "description": "Deletes a specified EBS Snapshot",
    "resourceTypes": [
      "EBS Snapshot"
    ],
    "params": [
      {
        "name": "DryRun",
        "type": "boolean",
        "default": "true"
      }
    ],
    "permissions": [
      "ec2:DeleteSnapshot"
    ]
  }

  return INFO