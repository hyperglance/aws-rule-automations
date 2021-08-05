import boto3
import json
import logging
from processing.automation_routing import *

## Setup Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TEST_MODE = False

def get_payload_from_s3(bucket, key):
  s3 = boto3.resource('s3')
  payload_object = s3.Object(bucket, key)
  payload_content = payload_object.get()['Body'].read().decode('utf-8')
  return json.loads(payload_content)

def put_report_to_s3(bucket, key_prefix, report):
  automation_name = report['name']
  num_successful = len(report['processed'])
  num_errored = len(report['errored'])
  total = num_successful + num_errored
  report_name = f'report_{automation_name}_total({total})_success({num_successful})_error({num_errored}).json'

  payload_json = json.dumps(report)
  s3 = boto3.resource('s3')
  s3.Object(bucket, key_prefix + report_name).put(Body=payload_json)

# MAIN ENTRY POINT
def lambda_handler(event, context):
  # Lambda is triggered by SNS
  snsMessage = event if TEST_MODE else json.loads(event['Records'][0]['Sns']['Message'])
  logger.debug('%s', snsMessage)

  # Extract details about the S3 bucket and the event payload file
  bucket = snsMessage['data']['s3bucket']
  bucket_key = snsMessage['data']['key']

  # Vars used for reporting back to S3
  outputs_per_automation = [];
  report_key_prefix = '/'.join(bucket_key.split('/')[0:-1]) + '/'

  try:      
    ## Read the event payload in from S3
    automation_data = event if TEST_MODE else get_payload_from_s3(bucket, bucket_key)

    process_event(automation_data, outputs_per_automation)
  except Exception as err:
    msg = 'Failed to process Rule automations. %s' % err
    logger.exception(msg)

    # Report critical lambda failure back to Hyperglance
    # For now, we are doing this by creating a dummy automation report to convey the error message
    error_report = {'name':'critical_error', 'processed':[], 'errored':[], 'critical_error':msg}
    put_report_to_s3(bucket, report_key_prefix, error_report)
  finally:
    # Report back to Hyperglance, a file in S3 for each automation
    for report in outputs_per_automation:
      put_report_to_s3(bucket, report_key_prefix, report)
