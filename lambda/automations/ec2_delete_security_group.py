"""EC2 Delete Security Group

This automation Deletes a Security Group, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to Delte a Security Group

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  sg_id = resource['attributes']['Group ID']

  try:
    response = client.delete_security_group(
      GroupId=sg_id,
      DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes']
    )
    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      automation_output = "An unexpected error occurred, error message {}".format(result)
    else:
      automation_output = "Security Group {} deleted.".format(sg_id)

  except ClientError as err:
    automation_output = "An unexpected CLient Error Occured {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Delete Security Group",
    "description": "Deletes a specified Security Group",
    "resourceTypes": [
      "Security Group"
    ],
    "params": [

    ]
  }

  return INFO