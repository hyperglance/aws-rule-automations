"""generate permissions needed for all automations, specific to none

This module allows for the core permissions to be generated dynamically
"""


def info() -> dict:
  INFO = {
    "displayName": "",
    "description": "",
    "resourceTypes": [],
    "params": [
    ],
    "permissions": [
      "sts:AssumeRole"
    ]
  }

  return INFO