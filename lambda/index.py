import boto3
import json
import logging
from processing.automation_routing import *

## Setuo Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TEST_MODE = False

def get_payload_from_s3(bucket, key):
  s3 = boto3.resource('s3')
  payload_object = s3.Object(bucket, key)
  payload_content = payload_object.get()['Body'].read().decode('utf-8')
  return json.loads(payload_content)

def put_payload_to_s3(bucket, key, payload):
  payload_json = json.dumps(payload)
  s3 = boto3.resource('s3')
  s3.Object(bucket, key).put(Body=payload_json)

# Get SNS from Hyperglance, read file from SNS and Trigger the automations
def lambda_handler(event, context):
  output_payload = {'critical_error': None, "automations_report": []}

  try:  
    payload = event if TEST_MODE else json.loads(event['Records'][0]['Sns']['Message'])
    logger.debug('%s', payload)
    
    ## Read the event payload in from S3
    bucket = payload['data']['s3bucket']
    bucket_key = payload['data']['key']
    automation_data = event if TEST_MODE else get_payload_from_s3(bucket, bucket_key)

    process_event(automation_data, output_payload)
  except Exception as err:
    msg = 'Failed to process Rule automations. %s' % err
    logger.exception(msg)
    output_payload['critical_error'] = msg

  # Report back to Hyperglance
  put_payload_to_s3(bucket, bucket_key + '_completed', output_payload)
