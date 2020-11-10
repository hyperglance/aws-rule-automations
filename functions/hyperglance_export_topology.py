import os
import boto3
import logging
import urllib3
import datetime
from botocore.exceptions import ClientError
import json

# Disable Warnings
urllib3.disable_warnings()

# Set logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Save Returned File to S3 Storage
def hyperglance_saveToS3(topology):
    # Filename To Write
    FILENAME = "hyperglance-{}.png".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    # Upload the file to S3
    s3 = boto3.client("s3")
    try:
      logging.info('Saving {} to S3 Bucket: {}'.format(FILENAME, os.environ['BUCKET_NAME']))
      response = s3.put_object(Body=topology, Bucket=os.environ['BUCKET_NAME'], Key=FILENAME)
      logging.info(response)
    except ClientError as ex:
      logging.error(ex)
      return False
    return True

# Request Topology Drawing from Hyperglance
def hyperglance_requestTopology():
    logger.info('Requesting Export to PNG')
    REQUEST_URL = 'https://' + os.environ['HYPERGLANCE_IP'] + '/hgapi/export-png'
    AUTH_TOKEN = os.environ['API_KEY_NAME'] + ':' + os.environ['API_KEY']

    JSON = {
            "datasource": "Datasource_Group",
            "account": os.environ['EXPORT_ACCOUNT'],
            "id": os.environ['EXPORT_ID']
    }

    # Disable Certificate Checking for Self-Signed Cert
    http = urllib3.PoolManager(assert_hostname = False, cert_reqs = 'CERT_NONE')

    # Append the headers to the request
    headers = {'Content-Type':'application/json'}
    headers.update(urllib3.make_headers(basic_auth=AUTH_TOKEN))

    # Call the API
    result = http.request('POST',
                          REQUEST_URL,
                          body = json.dumps(JSON),
                          headers = headers, 
                          retries = False,
                          timeout = 30.0
                          )

    if result.status != 200:
      logger.error('Error Calling API: {}'.format(result.status))
      logger.error(result)

    return hyperglance_saveToS3(result.data);


def handler(event, context):
    return hyperglance_requestTopology()