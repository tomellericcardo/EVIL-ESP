# -*- coding: utf-8 -*-

from machine import Pin
from time import sleep_ms


class Button:

  def __init__(self, config):
    if config['enabled']:
      pin = config['pin']
      self.button = Pin(pin, Pin.IN, Pin.PULL_UP)

  def button_pressed(self):
    return self.button.value() == 0

  def check_input(self):
    if self.button_pressed():
      sleep_ms(300)
      if self.button_pressed():
        return 2
      return 1
    return 0

  def wait_input(self, max = 0.3):
    counter = 0
    press = self.check_input()
    while press == 0 and counter < max:
      sleep_ms(50)
      counter += 0.1
      press = self.check_input()
    return press
