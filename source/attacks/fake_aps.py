# -*- coding: utf-8 -*-

from urandom import getrandbits
from time import sleep_ms


PACKET = [
  0x80, 0x00, 0x00, 0x00,                                 #  0 - 3  : Type, Subtype (Beacon Frame)
  0xff, 0xff, 0xff, 0xff, 0xff, 0xff,                     #  4 - 9  : Destionation Address (broadcast)
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00,                     # 10 - 15 : Source Address
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00,                     # 16 - 21 : Source Address
  0x00, 0x00,                                             # 22 - 23 : Sequence Control
  0x83, 0x51, 0xf7, 0x8f, 0x0f, 0x00, 0x00, 0x00,         # 24 - 31 : Timestamp
  0xe8, 0x03,                                             # 32 - 33 : Interval (0x64, 0x00 : 100ms, 0xe8, 0x03 : 1s)
  0x31, 0x00,                                             # 34 - 35 : Capability Info
  0x00, 0x20                                              # 36 - 37 : ESSID Length
]

TAIL = [

  # Supported rates
  0x01, 0x08,
  0x82, 0x84, 0x8b, 0x96,
  0x24, 0x30, 0x48, 0x6c,

  # Channel
  0x03, 0x01,
  0x01,

  # RSN information
  0x30, 0x18,
  0x01, 0x00,
  0x00, 0x0f, 0xac, 0x02,
  0x02, 0x00,
  0x00, 0x0f, 0xac, 0x04, 0x00, 0x0f, 0xac, 0x04,
  0x01, 0x00,
  0x00, 0x0f, 0xac, 0x02,
  0x00, 0x00

]


class FakeAPs:

  def __init__(self, tools, config):
    self.tools = tools
    self.channel = config['channel']
    self.essids = config['essids']

  def set_random_mac(self, packet):
    for i in range(6):
      packet[10 + i] = packet[16 + i] = getrandbits(8)

  def new_packet(self, essid):
    global PACKET, TAIL
    packet = bytearray(PACKET)
    self.set_random_mac(packet)
    packet[37] = len(essid)
    packet.extend(essid)
    tail = bytearray(TAIL)
    tail[12] = self.channel
    packet.extend(tail)
    return packet

  def start(self):
    sent = 0
    channel = 10
    self.tools.station_active()
    while True:
      for essid in self.essids:
        packet = self.new_packet(essid)
        self.tools.send_packet(self.channel, packet, sent)
        sent += 1
      sleep_ms(5)
