"""Tags an EC2 Resource

This automation attempts to fix a tag in for an EC2 resource, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Tag an EC2 Resource

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

  target_key = list(matched_attributes.keys())[0]
  target_value = matched_attributes.get(target_key)
  new_key = automation_params.get('New Key')

  if target_key == new_key:
    ## Skip automation
    return "Target Key: {} is an exact match of New Key: {}, skipping the automation".format(target_key, new_key)
  
  ## Creat the new tag and retain existing value
  try:
    response = client.create_tags(
      Resources=[
        resource_id,
      ],
      DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes'],
      Tags=[
        {
          'Key': new_key,
          'Value': target_value
        },
      ]
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >=400:
      automation_output = "An unexpected error occured, error message: {}".format(result)
      return automation_output
    else:
      automation_output = "Added Tag: {} with Value: {} to Resource: {}".format(new_key, target_value, resource_id)
  
  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)
  
  ## Attempt to Delete the offending tag
  try:
    response = client.delete_tags(
      Resources=[
        resource_id,
      ],
      DryRun=automation_params.get('DryRun').lower() in ['true', 'y', 'yes'],
      Tags=[
        {
          'Key': target_key,
          'Value': target_value
        },
      ]
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      automation_output += " An Unexpected error occured, error message: {}".format(result)
      return automation_output
    else:
      automation_output += " Removed Tag: {} from Resource: {}".format(target_key, resource_id)

  except ClientError as err:
    automation_output = "An unexpected client error occured, error: {}".format(err)
    return automation_output


  return automation_output