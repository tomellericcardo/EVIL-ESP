# -*- coding: utf-8 -*-

import ujson as json
import gc
import machine

from interface import Interface, Voice
from tools import Tools
from attacks import Attacks


class Main:

  def __init__(self):
    self.config = self.load_config()
    self.interface = Interface(self.config['interface'])
    self.tools = Tools(self.interface, self.config['tools'])
    self.attacks = Attacks(self.tools, self.config['attacks'])
    self.tools.stop_interfaces()

  def load_config(self):
    with open('data/config/config.json') as f:
      return json.load(f)

  def main_interface(self):
    return self.interface.show('EVIL-ESP', [
      Voice('Options', self.options_interface),
      Voice('Attacks', self.attacks_interface),
      Voice('Logs', self.logs_interface)
    ])

  def options_interface(self):
    return self.interface.show('OPTIONS', [
      Voice('Back', self.main_interface),
      Voice('Config Mode', self.tools.start_config_mode),
      Voice('Sleep', self.device_sleep)
    ])

  def attacks_interface(self):
    return self.interface.show('ATTACKS', [
      Voice('Back', self.main_interface),
      Voice('Beacon Spammer', self.attacks.start_beacon_spammer),
      Voice('Captive Portal', self.attacks.start_captive_portal),
      Voice('Evil Twin', self.evil_twin_interface)
    ])

  def create_lambda(self, essid):
    return lambda: self.attacks.start_evil_twin(essid)

  def evil_twin_interface(self):
    self.interface.show_single(['Scanning'])
    voices = [Voice('No networks', self.attacks_interface)]
    networks = self.tools.scan_networks()
    if len(networks) > 0:
      voices[0].name = 'Back'
      for net in networks:
        if net[4] > 0:
          essid = str(net[0], 'utf-8')
          callback = self.create_lambda(essid)
          voices.append(Voice(essid, callback))
    return self.interface.show('TWIN', voices)

  def logs_interface(self):
    return self.interface.show('LOGS', [
      Voice('Back', self.main_interface),
      Voice('Captive Portal', self.captive_portal_logs_interface),
      Voice('Evil Twin', self.evil_twin_logs_interface)
    ])

  def captive_portal_logs_interface(self):
    voices = [Voice('No credentials', self.logs_interface)]
    logs = self.attacks.get_captive_portal_logs()
    if len(logs) > 0:
      voices = []
      for log in logs:
        log = log.replace('\n', '')
        voices.append(Voice(log, self.logs_interface))
    return self.interface.show('PORTAL', voices)

  def evil_twin_logs_interface(self):
    voices = [Voice('No credentials', self.logs_interface)]
    logs = self.attacks.get_evil_twin_logs()
    if len(logs) > 0:
      voices = []
      for log in logs:
        log = log.replace('\n', '')
        voices.append(Voice(log, self.logs_interface))
    return self.interface.show('TWIN', voices)


  def device_sleep(self):
    self.interface.sleep_screen()
    machine.deepsleep()

  def start(self):
    display_enabled = self.config['interface']['display']['enabled']
    button_enabled = self.config['interface']['button']['enabled']
    default_attack = self.config['attacks']['default']
    if display_enabled and button_enabled:
      self.loop()
    elif default_attack == 'beacon_spammer':
      self.attacks.start_beacon_spammer
    elif default_attack == 'captive_portal':
      self.attacks.start_captive_portal
    elif default_attack == 'evil_twin':
      target_essid = self.config['attacks']['evil_twin']['default_essid']
      self.attacks.start_evil_twin(target_essid)

  def loop(self, callback = None):
    while True:
      if not callback:
        callback = self.main_interface
      callback = callback()


if __name__ == '__main__':
  main = Main()
  gc.collect()
  main.start()
