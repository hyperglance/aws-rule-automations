"""ELB Delete Load Balancer - V2

This action Deletes an Elastic Load Balancer, identified as above or below the configured threshold
by Hyperglance Rule(s)

This action will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_action(boto_session, rule: str, resource_id: str) -> str:
  """ Attempts to Delete and ELB Load Balancer

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