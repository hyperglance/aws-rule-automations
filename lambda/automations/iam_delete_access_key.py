"""
This automation Deletes a IAM User Access Key, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to delete a User Access Key

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """

  client = boto_session.client('iam')
  user_name = resource['attributes']['User Name']

  iam_user_access_keys = client.list_access_keys(
    UserName=user_name
  )

  for key in iam_user_access_keys['AccessKeyMetadata']:
    ## Get access key ID
    access_key_id = key['AccessKeyId']
    client.delete_access_key(
      UserName=user_name,
      AccessKeyId=access_key_id
    )


def info() -> dict:
  INFO = {
    "displayName": "Delete Access Keys",
    "description": "Deletes IAM Access Keys",
    "resourceTypes": [
      "IAM User"
    ],
    "params": [

    ]
  }

  return INFO
