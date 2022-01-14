import json
import logging
from processing.automation_routing import *
from s3.s3utils import get_payload_from_s3, put_report_to_s3, put_pending_status_to_s3, remove_pending_status_from_s3

## Setup Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TEST_MODE = False

# MAIN ENTRY POINT
def lambda_handler(event, context):
  # Lambda is triggered by S3 object subscription
  s3Event = event if TEST_MODE else event['Records'][0]['s3']
  logger.debug('%s', s3Event)

  # Extract details about the S3 bucket and the event payload file
  bucket = s3Event['bucket']['name']
  bucket_key = s3Event['object']['key']

  # Vars used for reporting back to S3
  outputs_per_automation = [];
  report_key_prefix = '/'.join(bucket_key.split('/')[0:-1]).replace('/events/', '/reports/') + '/'

  try:      
    ## Read the event payload in from S3
    automation_data = event if TEST_MODE else get_payload_from_s3(bucket, bucket_key)

    # Write a pending report into S3
    put_pending_status_to_s3(bucket, report_key_prefix)

    # Process main automations logic
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
    for index, report in enumerate(outputs_per_automation):
      put_report_to_s3(bucket, report_key_prefix, report, index)

    # Remove the pending signal file
    remove_pending_status_from_s3(bucket, report_key_prefix)
