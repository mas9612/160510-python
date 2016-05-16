#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import socket
import sys

import ProblemThread


def main():
    if len(sys.argv) < 2:
        print('few arguments')
        print('problem.py [port number]')
        sys.exit(1)

    if not sys.argv[1].isdigit():
        print('invalid port number')
        sys.exit(1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clients = set()

    host = '0.0.0.0'
    port = int(sys.argv[1])
    backlog = 10

    server.bind((host, port))
    server.listen(backlog)

    try:
        while True:
            conn, addr = server.accept()
            print('accept from {}'.format(addr))
            clients.add(conn)
            problem = ProblemThread.ProblemThread(conn)
            problem.start()
    except KeyboardInterrupt:
        print('Stop problem server.')
    finally:
        for c in clients:
            c.close()

if __name__ == '__main__':
    main()
