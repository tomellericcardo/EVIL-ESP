# -*- coding: utf-8 -*-

from network import WLAN, STA_IF, AP_IF


class Station:

  def __init__(self):
    self.sta_if = WLAN(STA_IF)

  def stop(self):
    self.sta_if.active(False)

  def active(self):
    self.sta_if.active(True)

  def send_packet(self, channel, packet):
    self.sta_if.freedom(channel, packet)

  def scan(self):
    self.sta_if.active(True)
    return self.sta_if.scan()


class AccessPoint:

  def __init__(self):
    self.ap_if = WLAN(AP_IF)

  def get_ip(self):
    return self.ap_if.ifconfig()[0]

  def stop(self):
    self.ap_if.active(False)

  def start(self, essid, password):
    self.ap_if.active(True)
    if password:
      self.ap_if.config(
        essid = essid,
        password = password,
        authmode = 4
      )
    else:
      self.ap_if.config(
        essid = essid,
        authmode = 0
      )
