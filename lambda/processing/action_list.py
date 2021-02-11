import os
import json

def get_action_list():
  action_path = '../actions'
  action_lists = os.listdir(action_path)
  action_list = [os.path.splitext(x)[0] for x in action_lists]

  action = '{"actions":'
  action += json.dumps(action_list)
  action += '}'

  return action