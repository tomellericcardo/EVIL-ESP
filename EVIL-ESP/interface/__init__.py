# -*- coding: utf-8 -*-

from .display import Display
from .button import Button


class Interface:

  def __init__(self, config):
    self.display = Display(config['display'])
    self.button = Button(config['button'])

  def sleep_screen(self):
    self.display.sleep_screen()

  def show(self, title, voices):
    current = 0
    self.display.counter = 0
    while True:
      self.display.show(title, voices, current)
      press = self.button.wait_input()
      if press == 1:
        current = (current + 1) % len(voices)
        self.display.counter = 0
      elif press == 2:
        return voices[current].callback

  def show_single(self, voices):
    self.display.show_single(voices)


class Voice:

  def __init__(self, name, callback):
    self.name = name
    self.callback = callback
