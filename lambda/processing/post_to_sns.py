import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_to_sns(boto_session, automation_ouput, sns_arn):
  logger.debug('Sending JSON to Topic: %s', sns_arn)

  sns_client = boto_session.client('sns')

  try:
    response = sns_client.publish(
      TopicArn=sns_arn,
      Message=json.dumps(automation_ouput),
      Subject='Hyperglance_Automation_Log',
      MessageStructure='string'
    )

    result = response['ResponseMetadata']['HTTPStatusCode']
    if result > 400:
      logger.error('Unable to Send SNS, error: %s', response)
    else:
      logger.debug('Sent Log SNS')
    
  except ClientError as err:
    logger.error('An unexpected client error occured, error: %s', err)

  