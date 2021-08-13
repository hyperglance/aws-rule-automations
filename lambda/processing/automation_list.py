"""Get Automation List

Returns the list of available automations for use in Hyperglance.
"""

import os
import importlib
import sys
import pathlib


def generate_json(lambda_root) -> list:
    """ Generates the HyperglanceAutomations.json file

  Returns
  -------
  list
    A json formatted list containing the available automations

  """
    automation_files = os.listdir(os.path.join(lambda_root, "automations"))
    automations = [os.path.splitext(x)[0] for x in automation_files]
    root = {"automations": []}

    for index, automation in enumerate(automations):
        automation_module = importlib.import_module(''.join(['automations.', automation]), package=None)
        automation_info = {"name": automation}
        automation_info.update(automation_module.info())
        root["automations"].append(automation_info)
    return str(root).replace("'", "\"")


automations_file = pathlib.Path(os.path.abspath(__file__)).parents[2].joinpath("files/HyperglanceAutomations.json")
lambda_root = pathlib.Path(os.path.abspath(__file__)).parents[1]

file = open(automations_file, "w")
sys.path.append(str(lambda_root))
file.write(generate_json(lambda_root))
file.close()

print(''.join(['{"automation_file":', '"', str(automations_file), '"}']))  # terraform quirks
