## elb_delete_load_balancer

## Deletes load balancers identified by configured Hyperglance Rules.
import boto3

## Delete ELB
def hyperglance_action(boto_session, rule, entity, params):
  ## TODO: Add conditional logic for Classic ELB 
  client = boto_session.client('elbv2')
  load_balancer = entity['id']

  response = client.delete_load_balancer(
    LoadBalancerArn=load_balancer
  )

  result = response['ResponseMetadata']['HttpStatusCode']
  if response >= 400:
    action_output = "An unexpected error occured, error messaage: {}".format(str(result))
  else:
    action_output = "Load Balancer {} stopped".format(load_balancer)

  return action_output