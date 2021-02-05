import os
import boto3
import re
import importlib
import json
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_payload_from_s3(bucket, key):
  s3 = boto3.resource('s3')
  payload_object = s3.Object(bucket, key)
  payload_content = payload_object.get()['Body'].read().decode('utf-8')
  payload_json = json.loads(payload_content)

  return payload_json

def process_event(bucket, action_payload):
  ## Read the Payload in from S3
  action_data = get_payload_from_s3(bucket=bucket, key=action_payload)
  # Check that threshold is actually 'ABOVE_THRESHOLD'
  logger.debug('Payload From S3 %s', action_data)
  logger.debug('Rule: %s', action_data['name'])
  
  ## Start Processing the Actions
  action_to_execute_output = ''
  ## TODO: Remove this once the new Payload is available
  if not 'action' in action_data:
    action = 'ec2_stop_instance'
  else:
    action = action_data['action']
  
  ## For each of the results, execute the action
  for index, result in enumerate(action_data['results']):
    try:
      action_to_execute = importlib.import_module(''.join(['actions.', action]), package=None)
    except:
      logger.error('Unable to find action: %s, Please check action tag for errors', action)
      continue

    ## Get the session to pass to the actions
    try:
      action_sts = boto3.client('sts')
      ## Account ID where this functions lambda is running
      this_account_id = action_sts.get_caller_identity()['Account']
    except ClientError as err:
      logger.error('Unexpected STS Client Error Occured: %s', err)
      return False

    ## Get the account of the Resourece that raised the Alert
    action_account_id = result['account']

    ## TODO: Add conditionals
    boto_session = boto3.Session(region_name=result['region'])


    logger.debug('Instance: %s', result['id'])
    logger.debug('Account: %s', result['account'])
    ## Run the bot!
    try:
      action_to_execute_output = action_to_execute.hyperglance_action(boto_session=boto_session, rule=result['name'], resource_id=result['id'])
      logger.info('Executed %s successfully', action)
    except Exception as err:
      logger.fatal('Could not execute: %s, output from action: %s', action, action_to_execute_output)
      continue  

    return True