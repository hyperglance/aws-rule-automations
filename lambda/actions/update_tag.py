"""Tags an EC2 Resource

This action attempts to fix a tag in for an EC2 resource, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Tag an EC2 Resource

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  resource_id : str
    ID of the Resource to trigger the action on
  matched_attributes : 
    Matching attributes that caused the rule to trigger
  table : list
    A list of additional resource values that may be required
  action_params : str
    Action parameters passed from the Hyperglance UI

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')

  target_key = list(matched_attributes.keys())[0]
  target_value = matched_attributes.get(target_key)
  new_key = action_params.get('New Key')

  ## Attempt to Delete the offending tag
  try:
    response = client.delete_tags(
      Resources=[
        resource_id,
      ],
      Tags=[
        {
          'Key': target_key,
          'Value': target_value
        },
      ]
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_output = "An Unexpected error occured, error message: {}".format(result)
      return action_output
    else:
      action_output = "Removed Tag: {} from Resource: {}".format(target_key, resource_id)

  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)
    return action_output

  ## Creat the new tag and retain existing value
  try:
    response = client.create_tags(
      Resources=[
        resource_id,
      ],
      Tags=[
        {
          'Key': new_key,
          'Value': target_value
        },
      ]
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >=400:
      action_output += "An unexpected error occured, error message: {}".format(result)
      return action_output
    else:
      action_output += "Added Tag: {} with Value: {} to Resource: {}".format(new_key, target_value, resource_id)
  
  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)

  return action_output