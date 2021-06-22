"""ELB Delete Load Balancer - V2

This automation Deletes an Elastic Load Balancer, identified as above or below the configured threshold
by Hyperglance Rule(s)

This automation will operate across accounts, where the appropriate IAM Role exists.

"""

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  """ Attempts to Delete and ELB Load Balancer

  Parameters
  ----------
  boto_session : object
    The boto session to use to invoke the automation
  resource: dict
    Dict of  Resource attributes touse in the automation
  automation_params : str
    Automation parameters passed from the Hyperglance UI
  """
  ## TODO: Add conditional logic for Classic ELB 
  client = boto_session.client('elbv2')
  load_balancer = resource['id']

  client.delete_load_balancer(
    LoadBalancerArn=load_balancer
  )


def info() -> dict:
  INFO = {
    "displayName": "Delete Load Balancer",
    "description": "Destroys ALB/NLB Elastic Load Balancer (v2)",
    "resourceTypes": [
      "Application Load Balancer",
      "Network Load Balancer"
    ],
    "params": [

    ]
  }

  return INFO