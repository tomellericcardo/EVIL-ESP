# -*- coding: utf-8 -*-

from .captive_portal import CaptivePortal
from .evil_twin import EvilTwin


class Attacks:

  def __init__(self, tools, config):
    self.captive_portal = CaptivePortal(tools, config['captive_portal'])
    self.evil_twin = EvilTwin(tools, config['evil_twin'])

  def start_captive_portal(self):
    self.captive_portal.start()

  def start_evil_twin(self, essid):
    self.evil_twin.start(essid)

  def get_captive_portal_logs(self):
    with open('data/captive_portal/log.csv') as f:
      return f.readlines()

  def get_evil_twin_logs(self):
    with open('data/evil_twin/log.csv') as f:
      return f.readlines()
