
import importlib
import logging
from processing.automation_session import *


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def execute_on_resource(automation_to_execute, resource, action_params, this_account_id):
  ## Grab the account and region (some resources don't have a region, default to us-east-1)
  automation_account_id = resource['account']
  automation_region = resource['region'] if 'region' in resource else 'us-east-1'
  
  logger.debug('Begin resource %s in account %s for region %s', resource['uid'], automation_account_id, automation_region)

  if this_account_id != automation_account_id:
    ## Get session from assume role
    logger.info('Resource in another account, attempting assume role for account: %s' %automation_account_id)
    boto_session = get_boto_session(
      target_account_id=automation_account_id, 
      target_region=automation_region
    )
  else:
    ## It's the same account, grab the session
    logger.info('Resource is local to this account')
    boto_session = boto3.Session(region_name=automation_region)

  ## Run the automation!
  return automation_to_execute.hyperglance_automation(
    boto_session=boto_session,
    resource=resource,
    automation_params=action_params
  )

def process_event(automation_data, output_payload):
  logger.debug('Payload From S3 %s', automation_data)
  logger.info('Triggered For Hyperglance Rule: %s', automation_data['name'])

  ## Get Account ID where this functions lambda is running
  this_account_id = boto3.client('sts').get_caller_identity()['Account']
  logger.debug('Got the account: %s', this_account_id)

  ## For each chunk of results, execute the automation
  for chunk in automation_data['results']:
    if not 'automation' in chunk:
      continue

    resources = chunk['entities']
    automation = chunk['automation']
    automation_name = automation['name']
    logger.debug('Begin processing automation: %s', automation_name)
    
    ## Augment the automation dict to track errors and add to the output, this gets reported back to Hyperglance
    automation['processed'] = []
    automation['errored'] = []
    automation['critical_error'] = None
    output_payload['automations_report'].append(automation)
    
    ## Dynamically load the module that will handle this automation
    try:
      automation_to_execute = importlib.import_module(''.join(['automations.', automation_name]), package=None)
    except:
      msg = 'Unable to find or load an automation called: %s' % automation_name
      logger.error(msg)
      automation['critical_error'] = msg
      return

    ## For each of Resource, execute the automation
    for resource in resources:
      try:
        action_params = automation.get('params', '')

        automation_to_execute_output = execute_on_resource(automation_to_execute, resource, action_params, this_account_id)

        automation['processed'].append(resource)
        logger.info('Executed %s successfully %s', automation_name, automation_to_execute_output)
        
      except Exception as err:
        logger.error('Could not execute: %s, output from automation: %s', automation_name, err)
        resource['error'] = str(err) # augment resource with an error field
        automation['errored'].append(resource)