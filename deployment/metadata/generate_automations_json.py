"""Get Automation List

Returns the list of available automations for use in Hyperglance.
"""

import os
import importlib
import sys
import pathlib
import json


def generate_json(src_root) -> str:
    """ Generates the HyperglanceAutomations.json file

  Returns
  -------
  list
    A json formatted list containing the available automations

  """
    automation_files = os.listdir(os.path.join(src_root, "actions"))
    automations = [os.path.splitext(f)[0] for f in automation_files if f.endswith('.py')]
    root = {"automations": []}

    for index, automation in enumerate(automations):
        automation_module = importlib.import_module(''.join(['actions.', automation]), package=None)
        automation_info = {"name": automation}
        automation_info.update(automation_module.info())
        root["automations"].append(automation_info)
    return str(root).replace("'", "\"")


automations_file = pathlib.Path(os.path.abspath(__file__)).parents[2].joinpath("files/HyperglanceAutomations.json")
src_root = pathlib.Path(os.path.abspath(__file__)).parents[2].joinpath('src')

file = open(automations_file, "w")
sys.path.append(str(src_root))
file.write(generate_json(src_root))
file.close()

print(json.dumps({'automation_file': str(automations_file)}))  # terraform quirks
