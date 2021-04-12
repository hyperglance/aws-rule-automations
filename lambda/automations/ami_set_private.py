"""AMI Set To Private

This automation Sets and AMI to Private for AMIs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to set an AMI to Private

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource_id : str
    ID of the Resource to trigger the automation on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  automation_params : str
    Automation parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')

  ami_id = resource_id
  owner_id = table[0]['Owner ID']

  ## Attempt to update AMI Properties

  try:
    response = client.modify_image_attribute(
      ImageId=ami_id,
      LaunchPermission={
        'Remove': [
          {
            "Group": 'all',
            "UserId": owner_id
          },
        ]
      }
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      automation_output = "An unexpected error occured, error message: {}".format(result)
    else:
      automation_output = "AMI {} set to private".format(ami_id)

  except ClientError as err:
    automation_output = "An Unexpected Client Error occured, error message: {}".format(err)

  return automation_output

def info() -> dict:
  INFO = {
    "displayName": "Set AMI to Private",
    "description": "Sets and AMI to Private if it is currently Public",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO