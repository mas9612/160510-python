#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# import select
import socket
import sys


WORD_FILE = 'words.txt'
WRONG_MAX = 3


def createAnswer(string):
    words = string.strip().split(',')
    words.sort()
    return ''.join(words)


def sendHelp(conn):
    conn.sendall('送られてきた文字列をカンマごとに分割し，ソートした上で連結して送ってください．\n'
                 .encode('utf-8'))
    conn.sendall('3回連続間違えるとゲームオーバーです．\n'.encode('utf-8'))
    conn.sendall('問題は"q:"で始まります．\n'.encode('utf-8'))
    conn.sendall('"q:"は除いて文字列処理をしてください．\n\n'.encode('utf-8'))
    conn.sendall('ex) q:dog,apple,lion\n'.encode('utf-8'))
    conn.sendall('上のような文字列が送られてきたら，下のような文字列をサーバーに送ります．\n'.encode('utf-8'))
    conn.sendall('appledoglion\n'.encode('utf-8'))
    conn.sendall('すべて正解すると，completeと送られてきます．\n'.encode('utf-8'))
    conn.sendall('--------------------------------------------\n\n'.encode('utf-8'))


def mainProblem(conn):
    with open(WORD_FILE, 'r') as f:
        for line in f:
            wrong = 0
            answer = createAnswer(line[2:])
            encoded = line.encode('utf-8')
            conn.sendall(encoded)

            while True:
                data = conn.recv(1024)
                if len(data) == 0:
                    break

                print('ans: ', answer)
                print('recv:', data.decode('utf-8'))
                if data.strip().decode('utf-8') == answer:
                    break
                else:
                    wrong += 1
                    if wrong >= WRONG_MAX:
                        conn.sendall('Game Over'.encode('utf-8'))
                        sys.exit(0)
                    conn.sendall(encoded)

    conn.sendall('complete'.encode('utf-8'))


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if len(sys.argv) < 2:
        print('few arguments')
        print('problem.py [port number]')
        sys.exit(1)

    if not sys.argv[1].isdigit():
        print('invalid port number')
        sys.exit(1)

    host = '0.0.0.0'
    port = int(sys.argv[1])

    server.bind((host, port))
    server.listen(10)
    # server.setblocking(False)

    conn, addr = server.accept()

    print('accept from {}'.format(addr))

    sendHelp(conn)
    mainProblem(conn)

if __name__ == '__main__':
    main()
