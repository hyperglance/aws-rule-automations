"""AMI Set To Private

This action Sets and AMI to Private for AMIs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str, table: list = [ ]) -> str:
  """ Attempts to set an AMI to Private

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on
  table : list
    A list of additional resource values that may be required

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
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "AMI {} set to private".format(ami_id)

  except ClientError as err:
    action_output = "An Unexpected Client Error occured, error message: {}".format(err)

  return action_output