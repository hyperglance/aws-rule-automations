import boto3
import json
import random

def get_payload_from_s3(bucket, key):
  s3 = boto3.resource('s3')
  payload_object = s3.Object(bucket, key)
  payload_content = payload_object.get()['Body'].read().decode('utf-8')
  return json.loads(payload_content)

def put_report_to_s3(bucket, key_prefix, report, index):
  processed_resources = report['processed']
  errored_resources = report['errored']
  all_resources = processed_resources + errored_resources

  automation_name = report['name']
  num_successful = len(processed_resources)
  num_errored = len(errored_resources)
  total = num_successful + num_errored
  accounts = ','.join(set(map(lambda resource: resource['account'], all_resources)))
  report_name = f'report_{automation_name}_total({total})_success({num_successful})_error({num_errored})_accounts({accounts})_{index}.json'

  payload_json = json.dumps(report)
  s3 = boto3.resource('s3')
  s3.Object(bucket, key_prefix + report_name).put(Body=payload_json)

def put_pending_status_to_s3(bucket, key_prefix):
  s3 = boto3.resource('s3')
  s3.Object(bucket, key_prefix +  'is_pending').put()

def remove_pending_status_from_s3(bucket, key_prefix):
  s3 = boto3.resource('s3')
  s3.Object(bucket, key_prefix +  'is_pending').delete()