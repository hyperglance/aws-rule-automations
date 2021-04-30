import os
import boto3
import re
import importlib
import json
import logging
from processing.automation_session import *
from processing.post_to_sns import *
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_payload_from_s3(bucket, key):
  s3 = boto3.resource('s3')
  payload_object = s3.Object(bucket, key)
  payload_content = payload_object.get()['Body'].read().decode('utf-8')
  payload_json = json.loads(payload_content)

  return payload_json

def process_event(bucket, automation_payload):
  ## Read the Payload in from S3
  automation_data = get_payload_from_s3(bucket=bucket, key=automation_payload)
  logger.debug('Payload From S3 %s', automation_data)
  logger.info('Triggering Rule: %s', automation_data['name'])
  
  ## Start Processing the automations
  automation_to_execute_output = ''

  ## For each of the results, execute the automation
  for index, result in enumerate(automation_data['results']):
    if not 'automation' in result:
      logger.debug("No Automation Defined for this Entity, move to next index")
      continue
    else:
      automation = result['automation']['name']
      logger.debug('automation Set to: %s', automation)
    
    try:
      automation_to_execute = importlib.import_module(''.join(['automations.', automation]), package=None)
    except:
      logger.error('Unable to find automation: %s, Please check automation tag for errors', automation)
      continue

    ## For each of Resource, execute the automation
    for entity, resource in enumerate(result['entities']):

      ## Get the session to pass to the automations
      try:
        automation_sts = boto3.client('sts')
        ## Account ID where this functions lambda is running
        this_account_id = automation_sts.get_caller_identity()['Account']
        logger.debug('Got the account: %s', this_account_id)
      except ClientError as err:
        logger.error('Unexpected STS Client Error Occured: %s', err)
        return False

      ## Get the account of the Resourece that raised the Alert
      automation_account_id = resource['account']
      logger.debug('Account of Resource: %s', automation_account_id)

      ## Check if we have a region, some automations don't have a region, default to us-east-1
      if not 'region' in resource:
        automation_region = 'us-east-1'
      else:
        automation_region = resource['region']

      if this_account_id != automation_account_id:
        ## Get session from assume role
        logger.info('Resource in another account, attempting assume role for account: %s' %automation_account_id)
        boto_session = get_boto_session(
          target_account_id=automation_account_id, 
          target_region=automation_region
        )
      else:
        ## It's the same account, grab the session
        logger.info('Resource is in this account, ')
        boto_session = boto3.Session(region_name=automation_region)

      ## Check if the Payload has sent params
      if not 'params' in result['automation']:
        logger.debug('No Params Sent')
        action_params = ''
      else:
        action_params = result['automation']['params']

      ## Construct the SNS Log Topic
      LOG_ARN = "arn:aws:sns:us-east-1:{}:{}-log".format(this_account_id, os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
      ## Run the automation!
      try:
        automation_to_execute_output = automation_to_execute.hyperglance_automation(
          boto_session=boto_session, 
          resource_id=resource['id'],
          matched_attributes=resource['matchedAttributes'], 
          table=resource['tables'],
          automation_params=action_params
          )
        logger.info('Executed %s successfully %s', automation, automation_to_execute_output)
        ## TODO: Add to a PASS [] List
        send_to_sns(
          boto_session,
          automation_to_execute_output,
          LOG_ARN
        )
      except Exception as err:
        logger.fatal('Could not execute: %s, output from automation: %s', automation, err)
        ## TODO: Add to a FAIL [] List
        send_to_sns(
          boto_session,
          automation_to_execute_output,
          LOG_ARN
        )
        continue

      ## Make one SNS call at the end of the run, passing the automation, PASS and FAIL LIST

  return automation_to_execute_output