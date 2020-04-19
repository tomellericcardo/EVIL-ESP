# -*- coding: utf-8 -*-

from usocket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


class Server:

  def __init__(self, interface, config):
    self.interface = interface
    self.max_users = config['max_users']
    self.dns_requests = 0
    self.get_requests = 0
    self.post_requests = 0
    self.set_udp_socket()
    self.set_tcp_socket()

  def set_udp_socket(self):
    self.udp_socket = socket(AF_INET, SOCK_DGRAM)
    self.udp_socket.setblocking(False)
    self.udp_socket.bind(('', 53))

  def set_tcp_socket(self):
    self.tcp_socket = socket(AF_INET, SOCK_STREAM)
    self.tcp_socket.settimeout(2)
    self.tcp_socket.bind(('', 80))
    self.tcp_socket.listen(self.max_users)

  def show_status(self):
    self.interface.show_single([
      self.title, 'Requests',
      'DNS :' + str(self.dns_requests),
      'GET :' + str(self.get_requests),
      'POST:' + str(self.post_requests),
    ])

  def dns_packet(self, data, domain):
    packet = b''
    if domain:
      packet += data[:2] + b'\x81\x80'
      packet += data[4:6] + data[4:6] + b'\x00\x00\x00\x00'
      packet += data[12:]
      packet += b'\xc0\x0c'
      packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
      packet += bytes(map(int, self.ip_address.split('.')))
    return packet

  def dns_response(self, data):
    type = (data[2] >> 3) & 15
    if type == 0:
      ini = 12
      lon = data[ini]
      domain = ''
      while lon != 0:
        i = ini + 1
        j = i + lon
        domain += data[i:j].decode('utf-8')
        domain += '.'
        ini += lon + 1
        lon = data[ini]
    return self.dns_packet(data, domain)

  def handle_udp(self):
    try:
      data, address = self.udp_socket.recvfrom(2048)
      response = self.dns_response(data)
      self.udp_socket.sendto(response, address)
      self.dns_requests += 1
    except:
      pass

  def parse_request(self, request_body):
    request_data = {}
    request_body = request_body.split('s=s&')[1]
    for argument in request_body.split('&'):
      key_value = argument.split('=')
      key = key_value[0]
      value = key_value[1]
      request_data[key] = value
    return request_data

  def send_page(self, connection):
    connection.send('HTTP/1.1 200 OK\n')
    connection.send('Content-Type: text/html\n')
    connection.send('Connection: close\n\n')
    connection.sendall(self.web_page)
    connection.close()

  def handle_tcp(self):
    try:
      connection, address = self.tcp_socket.accept()
      request = str(connection.recv(2048), 'utf-8')
      if request.split(' ')[0] == 'POST':
        request_body = str(connection.recv(2048), 'utf-8')
        request_data = self.parse_request(request_body)
        self.post_callback(request_data)
        self.post_requests += 1
      else:
        self.get_requests += 1
      self.send_page(connection)
    except:
      pass

  def start(self, ip_address, title, web_page, post_callback):
    self.ip_address = ip_address
    self.title = title
    self.web_page = web_page
    self.post_callback = post_callback
    while True:
      self.show_status()
      self.handle_udp()
      self.handle_tcp()
