"""Spits debug logging out and doesn't actually automate anything"""

import logging

logger = logging.getLogger()

def hyperglance_automation(boto_session, resource: dict, automation_params = ''):
  logger.info(resource)