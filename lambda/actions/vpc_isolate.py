"""
This action Qurantines a VPC, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError
import json


def attach_policy(boto_session, policy_arn: str) -> str:
  """ Attempts to Attach the policy to users

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  policy_arn : str
    Policy to attach to the user

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')

  account_users = client.list_users()['Users']

  try:
    ## Attache policy to each user
    for user in account_users:
      client.attach_user_policy(
        UserName=user.get('UserName'),
        PolicyArn=policy_arn
      )

    action_output = "VPC Isolated"

  except ClientError as err:
    action_output = "An unexpected client error has occured, error: {}".format(err)

  return action_output


def create_deny_policy(boto_session, region: str, vpc_id: str) -> str:
  """ Attempts to Create a deny policy for User attachment

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  region : str
    Target VPC Region
  vpc_id: str
    ID of the target VPC

  Returns
  -------
  string
    A string containing the status of the request

  """

  client = boto_session.client('iam')

  ## Policy Definition
  policy = {
    "Version": "2012-10-17",
    "Statement": [
      "Action": "ec2:*",
      "Effect": "Deny",
      "Resource": [
        "arn:aws:ec2:{region}:*vpc/{vpc_id}",
        "arn:aws:ec2:{}:*:security-group/*"
      ],
      "Condition": {
        "ArnEquals": {
          "ec2:Vpc": "arn:aws:ec2:{}:*:vpc/{}".format(region, vpc_id)
        }
      }
    ]
  }

  try:
    ## Create the policy
    client.create_policy(
      PolicyName="isolate_{}_access_policy".format(vpc_id),
      PolicyDocument=json.dumps(policy)
    )

  except ClientError as err:
    action_output = "An unexpected client error: {} has occured, unable to create policy".format(err)

  action_output = " "

  return action_output


def isolation_policy_exists(boto_session, policy_arn: str) -> bool:
  """ Checks if the isolation policy already exists

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the action
  policy_arn : str
    Policy ARN to check

  Returns
  -------
  bool
    Returns True if policy exists, otherwise False

  """

  client = boto_session.client('iam')

  try:
    client.get_policy(
      PolicyARN=policy_arn
    )
  
  except ClientError as err:
    if err.response['Error']['Code'] == 'NoSuchIdentity':
      return False
    else:
      return "An unexpected client error occured: {} cannot check for policy: {}".format(err, policy_arn)

  return True

def create_isolation_acl(client, vpc_id: str) -> str:
  """ Attempts to Create an Isolation ACL

  Parameters
  ----------
  client : object
    The boto client object
  vpc_id : str
    Id of target VPC

  Returns
  -------
  string
    A string containing the status of the request

  """

  ## VPC Subnets
  vpc_subnet_associations = [ ]

  try:
    acls = client.describe_network_acls(
      Filters=[
        {
          'Name': 'vpc-id',
          'Values': [
            vpc_id
          ]
        },
      ],
    )

    ## Iterate through each ACL
    for acl in acls.get('NetworkAcls'):
      associations = acl.get('Associations')
      if associations:
        vpc_subnet_associations += [associations.get('NetworkAclAssociationId') for association in associations]

    if vpc_subnet_associations:
      ## Create ACL with Deny ALL
      network_acl = client.create_network_acl(
        VpcId=vpc_id
      )

      for subnet_id in vpc_subnet_associations:
        client.replace_network_acl_association(
          AssociationId=subnet_id,
          DryRun=True,
          NetworkAclId=network_acl.get('NetowrkAclId')
        )

  except ClientError as err:
    action_output = "An unexepcted client error occured: {}, failed to create isolation acls".format(err)

  action_output = " "

  return action_output


def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Qurantine and EC2 Instance

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

  vpc_id = resource_id
  region = table[0]['Region']

  try:
    target_vpc = client.describe_vpcs(
      VpcIds=[vpc_id],
    ).get('Vpcs')[0]

    vpc_account_id = target_vpc.get('OwnerId')
    isolate_policy_arn = "arn:aws:iam::{}:policy/isolate_{}_access_policy".format(vpc_account_id, vpc_id)

    ## Disable DNS
    client.modify_vpc_atribute(
      EnableDnsSupport={
        'Value': False
      },
      VpcId=vpc_id
    )

    ## Create a Deny ACL
    action_output = create_isolation_acl(client, vpc_id)

    ## Check for Errors
    if action_output == ' ' and not isolation_policy_exists(
      boto_session=boto_session,
      policy_arn=isolate_policy_arn
      ):
      
      action_output = create_deny_policy(
        boto_session=boto_session,
        region=region,
        vpc_id=vpc_id
      )

      if 'error' in action_output:
        return action_output

    ## Attach policy to all users in the account
    action_output = attach_policy(
      boto_session=boto_session,
      policy_arn=isolate_policy_arn
    )

  except ClientError as err:
    action_output = "An unexpected client error occured, error: {}".format(err)

  return action_output


def info() -> dict:
  INFO = {
    "displayName": "Isolate VPC",
    "description": "Isolates an Entire VPC by applying Deny ALL security group rules",
    "resourceTypes": [
      "VPC"
    ],
    "params": [

    ]
  }

  return INFO