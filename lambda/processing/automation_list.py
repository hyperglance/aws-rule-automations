"""Get Action List

Returns the list of avaiblae actions for use in Hyperglance.
"""

import os
import json
import importlib
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



def update_automation_json(bucket) -> list:
  """ Generates a list of actions for sunsumption by Hyperglance.

  Returns
  -------
  list
    A json formatted list containing the available automations

  """
  automation_files = os.listdir(os.path.abspath("./automations"))
  automations = [os.path.splitext(x)[0] for x in automation_files]
  root = {"automations":[]}

  for index, automation in enumerate(automations):
    automation_module = importlib.import_module(''.join(['automations.', automation]), package=None)
    automation_info = automation_module.info()
    automation_info["name"] = automation
    root["automations"].append(automation_info)

  put_payload_to_s3(bucket, "HyperglanceAutomations.json", root)

def put_payload_to_s3(bucket, key, payload):
    payload_json = json.dumps(payload)
    s3 = boto3.resource('s3')
    s3.Object(bucket, key).put(Body=payload_json)


