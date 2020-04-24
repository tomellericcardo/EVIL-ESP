# -*- coding: utf-8 -*-

import gc


with open('data/captive_portal/log.csv') as f:
  print('\n *** PORTAL LOG ***')
  print(f.read())

with open('data/evil_twin/log.csv') as f:
  print('\n ***  TWIN LOG  ***')
  print(f.read())

gc.collect()
