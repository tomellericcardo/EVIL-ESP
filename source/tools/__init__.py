# -*- coding: utf-8 -*-

from time import sleep_ms

from .interfaces import AccessPoint, Station
from .server import Server


class Tools:

  def __init__(self, interface, config):
    self.interface = interface
    self.server = Server(interface, config['server'])
    self.access_point = AccessPoint()
    self.station = Station()

  def station_active(self):
    self.station.active()

  def send_packet(self, channel, packet, sent):
    self.station.send_packet(channel, packet)
    if sent % 50 == 0:
      self.interface.show_single([
        'FAKE APs', 'Packets:', str(sent)
      ])

  def start_server(self, title, web_page, post_callback):
    ip_address = self.access_point.get_ip()
    self.server.start(ip_address, title, web_page, post_callback)

  def stop_interfaces(self):
    self.access_point.stop()
    self.station.stop()

  def scan_networks(self):
    return self.station.scan()

  def start_ap(self, essid, password = None):
    self.access_point.start(essid, password)
