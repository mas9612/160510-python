#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import socket
import sys


HOST = '0.0.0.0'
PORT = 55555

WORD_FILE = 'words.txt'
WRONG_MAX = 3


def createAnswer(string):
    words = string.split(',')
    words.sort()
    return ''.join(words)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen(1)

    conn, addr = server.accept()

    with open('WORD_FILE', 'r') as f:
        for line in f:
            wrong = 0
            answer = createAnswer(line)
            encoded = line.encode('utf-8')
            conn.sendall(encoded)

            while True:
                data = conn.recv(1024)
                if len(data) == 0:
                    break

                if data.decode('utf-8') == answer:
                    break
                else:
                    wrong += 1
                    if wrong >= WRONG_MAX:
                        conn.sendall('Game Over'.encode('utf-8'))
                        sys.exit(0)
                    conn.sendall(encoded)

    conn.sendall('\n\nCongratulations!'.encode('utf-8'))
    conn.sendall('You solved all problems!'.encode('utf-8'))


if __name__ == '__main__':
    main()
