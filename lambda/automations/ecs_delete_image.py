"""ECS Delete Repository Image

This automation Sets and AMI to Private for AMIs, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""


def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to delete and ECS Repository Image

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('ecr')

  registry_id = resource['attributes']['Registry ID']
  repository_name = resource['attributes']['Repository Name']
  image_name = resource['attributes']['Image Name']
  image_digest = resource['attributes']['Image Digest']


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