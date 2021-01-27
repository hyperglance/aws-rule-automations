import json
import boto3
import logging

# Setup Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# EC2 Client
ec2_client = boto3.Client('ec2')

# Terminate the ec2 Instance
def hyperglance_ec2_terminate():
  # Log the rewuest
  hgAlert = json.parse(event.Records[0].Sns.Message)

  logger.info(
    'Recieved Hyperglasnce alert from saved-search.\n',
    '(',
    'Name: ', hgAlert.name. '\n',
    'Pack: ', hgAlert.pack, '\n',
    'Description: ', hgAlert.description, '\n',
    'Status: ', hgAlert.status, '\n',
    'Threshold: ', hgAlert.threshold, '\n',
    'Evaluation Time: ', hgAlert.evaluatedAt, '\n',
    'Num Results: ', hgAlert.results.length,
    ' )'
  )

  # Check alert level and only action threshold 
  if hgAlert.status != 'ABOVE_THRESHOLD' && hgAlert.status != 'BELOW_THRESHOLD':
      logger.info('Status was {}, so exiting with nothing to do'.format(hgAlert.status))
      return
  
  if snapshot:
      # Snapshot VM
  
  # Terminate Instances
    

def handler(event, context):
  for hgAlert in event['Records']:
    logger.info(hgAlert.status)
  return hyperglance_ec2_terminate