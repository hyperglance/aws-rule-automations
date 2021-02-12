"""Get Action List

Returns the list of avaiblae actions for use in Hyperglance.
"""

import os
import json

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

  action = '{"actions":'
  action += json.dumps(action_list)
  action += '}'

  ## TODO: Save to S3 Bucket 
  
  return action