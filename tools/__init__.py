# -*- coding: utf-8 -*-

from .interfaces import AccessPoint, Station
from .server import Server


class Tools:

  def __init__(self, interface, config):
    self.server = Server(interface, config['server'])
    self.access_point = AccessPoint()
    self.station = Station()

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
