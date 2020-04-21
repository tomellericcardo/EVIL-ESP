# -*- coding: utf-8 -*-

from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep_ms


class Display:

  def __init__(self, config):
    self.enabled = config['enabled']
    if self.enabled:
      pins = config['pins']
      size = config['size']
      i2c = I2C(-1, Pin(pins[0]), Pin(pins[1]))
      self.display = SSD1306_I2C(size[0], size[1], i2c)
      self.counter = 0
      self.rows = size[1] // 8
      self.cols = size[0] // 8

  def sleep_screen(self):
    self.display.fill(0)
    self.display.text('Going to', 0, 0)
    self.display.text('sleep...', 0, 8)
    self.display.show()
    sleep_ms(1000)
    self.display.fill(0)
    self.display.show()

  def format_voice(self, voice_obj, current):
    voice = voice_obj.name
    new_voice = ' ' + voice
    if current:
      new_voice = '.'
      if len(voice) > (self.cols - 1):
        for j in range(self.cols - 1):
          voice += ' '
        offset = self.counter % (len(voice) - (self.cols - 2))
        for j in range(offset, len(voice)):
          new_voice += voice[j]
      else:
        new_voice += voice
    return new_voice

  def show(self, title, voices, current):
    self.display.fill(0)
    self.display.text(title, 0, 0)
    j = (current // (self.rows - 1)) * (self.rows - 1)
    for i in range(j, len(voices)):
      voice = self.format_voice(voices[i], i == current)
      self.display.text(voice, 0, 8 * ((i - j) + 1))
    self.display.show()
    if self.counter == 0:
      sleep_ms(250)
    self.counter += 1

  def show_single(self, voices):
    if self.enabled:
      self.display.fill(0)
      for i in range(len(voices)):
        voice = voices[i]
        self.display.text(voice, 0, 8 * i)
      self.display.show()
