"""ELB Delete Load Balancer - V2

This action Deletes an Elastic Load Balancer, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_action(boto_session, resource_id: str, matched_attributes ='', table: list = [ ], action_params = '') -> str:
  """ Attempts to Delete and ELB Load Balancer

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
  ## TODO: Add conditional logic for Classic ELB 
  client = boto_session.client('elbv2')
  load_balancer = resource_id

  response = client.delete_load_balancer(
    LoadBalancerArn=load_balancer
  )

  result = response['ResponseMetadata']['HttpStatusCode']
  if response >= 400:
    action_output = "An unexpected error occured, error messaage: {}".format(result)
  else:
    action_output = "Load Balancer {} stopped".format(load_balancer)

  return action_output


def info() -> str:
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