#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import socket
import sys

port = int(sys.argv[1])
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', port))

while True:
    data = client.recv(1024)
    if len(data) == 0:
        break

    data = data.strip().decode('utf-8')
    if data.startswith('q:'):
        data = data[2:].split(',')
        data.sort()

        s = ''.join(data)
        client.sendall(s.encode('utf-8'))
        print('send:', s)
    else:
        print(data)

client.close()
