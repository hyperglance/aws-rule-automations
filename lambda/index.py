import json
import logging
from processing.action_routing import *

## Setuo Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEV_MODE = False  

# Get SNS from Hyperglance, read file from SNS and Triggrt Actions
def lambda_handler(event, context):
  
  payload = ''
  return_message = {}

  logger.info('Started Processing Payload')

  message = event['Records'][0]['Sns']['Message']

  try:
    if DEV_MODE:
      payload = event
    else:
      payload = json.loads(message)
      logger.debug('%s', payload)
  except:
    logger.error('Parsing message, failed to load: %s', event)
    return

  ## Some DEBUG Code, to check parsing
  logger.debug('Bucket: %s', payload['data']['s3bucket'])
  logger.debug('File: %s', payload['data']['key'])

  # Try to process the message, and perform actions
  try:
    return_message = process_event(bucket=payload['data']['s3bucket'], action_payload=payload['data']['key'])
  except Exception as err:
    logger.error('Failed to process Event %s', err )
    return_message['Failed to Process Event'] = str(err)

  return return_message  