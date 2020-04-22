# -*- coding: utf-8 -*-

from .interfaces import AccessPoint, Station
from .server import Server
from .config_mode import ConfigMode


class Tools:

  def __init__(self, interface, config):
    self.interface = interface
    self.access_point = AccessPoint()
    self.station = Station()
    self.server = Server(interface, config['server'])
    self.config_mode = ConfigMode(config['config_mode'])

  def stop_interfaces(self):
    self.access_point.stop()
    self.station.stop()

  def station_active(self):
    self.station.active()

  def scan_networks(self):
    return self.station.scan()

  def send_packet(self, channel, packet, sent):
    self.station.send_packet(channel, packet)
    if sent % 50 == 0:
      self.interface.show_single([
        'SPAMMER', 'Packets:', str(sent)
      ])

  def start_ap(self, essid, password = None):
    self.access_point.start(essid, password)

  def start_server(self, title, get_page, post_callback):
    ip_address = self.access_point.get_ip()
    self.server.start(
      ip_address,
      title,
      get_page(),
      post_callback
    )

  def start_config_mode(self):
    self.start_ap(
      self.config_mode.essid,
      self.config_mode.password
    )
    self.start_server(
      'CONFIG',
      self.config_mode.get_page,
      self.config_mode.update_config
    )
