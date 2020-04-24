# -*- coding: utf-8 -*-

import ujson as json
import gc


class ConfigMode:

  def __init__(self, config):
    self.essid = config['essid']
    self.password = config['password']
    self.main_config = self.load_config()

  def load_config(self):
    with open('data/config/config.json') as f:
      return json.load(f)

  def get_page(self):
    with open('data/config/page.html') as f:
      return f.read()

  def update_config(self, request):
    type = request['type']
    if type == 'beacon_spammer':
      self.main_config['attacks']['beacon_spammer']['channel'] = int(request['beacon_spammer_channel'])
      self.main_config['attacks']['beacon_spammer']['essids'] = request['beacon_spammer_essids'].split('\n')
    elif type == 'captive_portal':
      self.main_config['attacks']['captive_portal']['lang'] = request['captive_portal_lang']
      self.main_config['attacks']['captive_portal']['essid'] = request['captive_portal_essid']
    elif type == 'evil_twin':
      self.main_config['attacks']['evil_twin']['lang'] = request['evil_twin_lang']
    with open('data/config/config.json', 'w') as f:
      f.write(json.dumps(self.main_config))
