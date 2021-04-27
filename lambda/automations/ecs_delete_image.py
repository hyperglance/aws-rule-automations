"""ECS Delete Repository Image

This automation Sets and AMI to Private for AMIs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

from botocore.exceptions import ClientError

def hyperglance_automation(boto_session, resource: dict, automation_params = '') -> str:
  """ Attempts to delete and ECS Repository Image

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

  client = boto_session.client('ecr')

  registry_id = resource['attributes']['Registry ID']
  repository_name = resource['attributes']['Repository Name']
  image_name = resource['attributes']['Image Name']
  image_digest = resource['attributes']['Image Digest']

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

    automation_output = "Deleted ECR Image: {} from repository: {}".format(image_name, repository_name)

  except ClientError as err:
    automation_output = "An unexpected Client Error occured, error message: {}".format(err)

  return automation_output


def info() -> dict:
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