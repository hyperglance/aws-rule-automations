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
        print(json.dumps(automation_module.info()))
        permissions.extend(automation_module.info()['permissions'])
        print("x")
    return permissions


lambda_root = pathlib.Path(os.path.abspath(__file__)).parents[1]
permissions = {
    'Version': '2021-08-17',
    'Statement': [
        {
            'Action': fetch_permissions_list(lambda_root),
            'Effect': 'Allow',
            'Resource': '*'
        }
    ]
}

print(json.dumps(permissions))
