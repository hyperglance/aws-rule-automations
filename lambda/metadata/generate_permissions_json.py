"""Get the aggregated permissions required to run all automations

Returns list (json) of all required permissions
"""

import importlib
import json
import os
import pathlib
import sys


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
        permissions.extend(automation_module.info()['permissions'])
    return permissions


def insert(source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]


lambda_root = pathlib.Path(os.path.abspath(__file__)).parents[1]
sys.path.append(str(lambda_root))

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
permission_dump = json.dumps(permissions)

print(insert(permission_dump, ',', len(permission_dump) - 2))
