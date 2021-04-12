"""EC2 Delete Key Pair

This automation Deletes a Key Pair, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Delete a Key Pair

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
  keypair = resource_id

  try:
    response = client.delete_key_pair(
      KeyName=keypair
    )

    automation_output = "KeyPair {} was deleted successfully".format(keypair)

  except ClientError as err:
    automation_output = "An unexpected error occured, error message: {}".format(err)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Delete EC2 Key Pair",
    "description": "Deletes a specified EC2 Key Pair",
    "resourceTypes": [
      "EC2 Instance"
    ],
    "params": [

    ]
  }

  return INFO