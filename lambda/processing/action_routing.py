import os
import boto3
import re
import importlib
import json
import logging
from processing.action_list import *
from processing.action_session import *
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_payload_from_s3(bucket, key):
  s3 = boto3.resource('s3')
  payload_object = s3.Object(bucket, key)
  payload_content = payload_object.get()['Body'].read().decode('utf-8')
  payload_json = json.loads(payload_content)

  return payload_json

def process_event(bucket, action_payload):
  ## Read the Payload in from S3
  action_data = get_payload_from_s3(bucket=bucket, key=action_payload)
  logger.debug('Payload From S3 %s', action_data)
  logger.info('Triggering Rule: %s', action_data['name'])
  
  ## Start Processing the Actions
  action_to_execute_output = ''

  ## For each of the results, execute the action
  for index, result in enumerate(action_data['results']):
    if not 'remediation' in result:
      return "No Remediation Action Defined, ignoring...."
    else:
      action = result['remediation']['name']
      logger.debug('Action Set to: %s', action)
    
    try:
      action_to_execute = importlib.import_module(''.join(['actions.', action]), package=None)
    except:
      logger.error('Unable to find action: %s, Please check action tag for errors', action)
      continue

    ## For each of Resource, execute the action
    for entity, resource in enumerate(result['entities']):

      ## Get the session to pass to the actions
      try:
        action_sts = boto3.client('sts')
        ## Account ID where this functions lambda is running
        this_account_id = action_sts.get_caller_identity()['Account']
        logger.debug('Got the account: %s', this_account_id)
      except ClientError as err:
        logger.error('Unexpected STS Client Error Occured: %s', err)
        return False

      ## Get the account of the Resourece that raised the Alert
      action_account_id = resource['account']
      logger.debug('Account of Resource: %s', action_account_id)

      ## Check if we have a region, some actions don't have a region, default to us-east-1
      if not 'region' in resource:
        action_region = 'us-east-1'
      else:
        action_region = resource['region']

      if this_account_id != action_account_id:
        ## Get session from assume role
        logger.info('Resource in another account, attempting assume role for account: %s' %action_account_id)
        boto_session = get_boto_session(
          target_account_id=action_account_id, 
          target_region=action_region
        )
      else:
        ## It's the same account, grab the session
        logger.info('Resource is in this account, ')
        boto_session = boto3.Session(region_name=action_region)

      ## Run the action!
      try:
        action_to_execute_output = action_to_execute.hyperglance_action(
          boto_session=boto_session, 
          resource_id=resource['id'],
          matched_attributes=resource['matchedAttributes'], 
          table=resource['tables'],
          action_params=result['remediation']['params']
          )
        logger.info('Executed %s successfully %s', action, action_to_execute_output)
      except Exception as err:
        logger.fatal('Could not execute: %s, output from action: %s', action, err)
        continue  

  return action_to_execute_output