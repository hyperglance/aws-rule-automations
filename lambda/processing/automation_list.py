"""Get Action List

Returns the list of avaiblae actions for use in Hyperglance.
"""

import os
import json
import importlib


def get_action_list() -> list:
  """ Generates a list of actions for sunsumption by Hyperglance.

  Returns
  -------
  list
    A json formatted list containing the available actions

  """

  action_path = '../actions'
  action_lists = os.listdir(action_path)
  action_list = [os.path.splitext(x)[0] for x in action_lists]

  action_json = '{"actions": ['

  for index, action in enumerate(action_list):
    print(action)
    action_info = importlib.import_module(''.join(['lambda.actions.', action]), package=None)
    action_info_details = action_info.info()

    print(action_info_details)
  
    ##action_json += json.dumps(action_list)
    ##action_json += '}'

  ## TODO: Save to S3 Bucket 
  
  return action_json