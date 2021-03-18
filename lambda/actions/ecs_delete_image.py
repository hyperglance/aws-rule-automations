"""ECS Delete Repository Image

This action Sets and AMI to Private for AMIs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to delete and ECS Repository Image

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

  client = boto_session.client('ecr')

  registry_id = resource_id
  repository_name = table[0]['Repository Name']
  image_name = table[0]['Image Name']
  image_digest = table[0]['Image Digest']

  try:
    client.batch_delete_image(
      registryId=registry_id,
      respositoryName=repository_name,
      imageIds=[
        {
          'imageDigest' : image_digest,
          'imageTag' : image_name
        }
      ]
    )

    action_output = "Deleted ECR Image: {} from repository: {}".format(image_name, repository_name)

  except ClientError as err:
    action_output = "An unexpected Client Error occured, error message: {}".format(err)

  return action_output


def info() -> str:
  INFO = {
    "displayName": "Delete Container Image",
    "description": "Deletes and ECS Container Image",
    "resourceTypes": [
      "ECS Service"
    ],
    "params": [

    ]
  }

  return INFO