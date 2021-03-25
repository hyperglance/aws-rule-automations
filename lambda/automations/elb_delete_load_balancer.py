"""ELB Delete Load Balancer - V2

This automation Deletes an Elastic Load Balancer, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], automation_params = '') -> str:
  """ Attempts to Delete and ELB Load Balancer

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
  ## TODO: Add conditional logic for Classic ELB 
  client = boto_session.client('elbv2')
  load_balancer = resource_id

  response = client.delete_load_balancer(
    LoadBalancerArn=load_balancer
  )

  result = response['ResponseMetadata']['HttpStatusCode']
  if response >= 400:
    automation_output = "An unexpected error occured, error messaage: {}".format(result)
  else:
    automation_output = "Load Balancer {} stopped".format(load_balancer)

  return automation_output


def info() -> dict:
  INFO = {
    "displayName": "Deletes v2 Load Balancer",
    "description": "Destroys and Elastic Load Balancer (v2)",
    "resourceTypes": [
      "Elastic Load Balancer"
    ],
    "params": [

    ]
  }

  return INFO