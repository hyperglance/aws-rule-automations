
"""
This action Deletes all Ingress and Egress Securoty Group rules , identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to all Ingress and Egress Security Group Rules

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  rule : str
    Rule name that trigged the action
  resource_id : str
    ID of the Resource to trigger the action on

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('ec2')
  security_group_id = resource_id

  ## Get the Security Group Details
  security_group_description = client.describe_security_groups(
    GroupIds=security_group_id
  )

  ## Extract Ingress and Egress Rules for processing
  security_group_ingress = security_group_description['SecurityGroups'][0]['IpPermissions']
  security_group_egress = security_group_description['SecurityGroups'][0]['IpPermissionsEgress']

  resource_client = boto_session.resource('ec2')
  security_group_client = resource_client.SecurityGroup(security_group_id)

  ## Attempt to delete the the Egress Rules
  if security_group_egress:
    ## Reduce to just IDs
    for index, rules in enumerate(security_group_egress):
      try:
        del security_group_egress[index]['UserIdGroupsPairs'][0]['GroupName']
      except Exception as err:
        continue
    response = security_group_client.revoke_egress(
      IpPermissions=security_group_egress
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output = "Security Group: {} Egress Rules removed".format(security_group_id)

  ## Attempt to delete
  if security_group_ingress:
    ## Reduce to just IDs
    for index, rules in enumerate(security_group_ingress):
      try:
        del security_group_ingress[index]['UserIdGroupPairs'][0]['GroupName']
      except Exception as err:
        continue
    response = security_group_client.revoke_ingress(
      IpPermissions=security_group_ingress
    )

    result = response['ResponseMetadata']['HTTPStatusCode']

    if result >= 400:
      action_output = "An unexpected error occured, error message: {}".format(result)
    else:
      action_output += "Security Group: {} ingress rules removed".format(security_group_id)

  return action_output