"""Get the aggregated permissions required to run all automations

Returns list (json) of all required permissions
"""

import importlib
import json
import os
import pathlib


def fetch_permissions_list(lambda_root) -> list:
    """ Generates the HyperglanceAutomations.json file

  Returns
  -------
  list
    A json formatted list containing the available automations

  """
    automation_files = os.listdir(os.path.join(lambda_root, "automations"))
    automations = [os.path.splitext(f)[0] for f in automation_files if f.endswith('.py')]
    permissions = []

    for index, automation in enumerate(automations):
        automation_module = importlib.import_module(''.join(['automations.', automation]), package=None)
        print(automation)
        permissions.extend(automation_module.info()['permissions'])

    return permissions


lambda_root = pathlib.Path(os.path.abspath(__file__)).parents[1]
print(json.dumps({'Action': fetch_permissions_list(fetch_permissions_list(lambda_root))}))
