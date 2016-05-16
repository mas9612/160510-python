#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import threading


class ProblemThread(threading.Thread):
    WRONG_MAX = 3
    WORD_FILE = 'words.txt'

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        self.sendHelp(self.conn)
        self.mainProblem(self.conn)

    def sendHelp(self, conn):
        conn.sendall('送られてきた文字列をカンマごとに分割し，ソートした上で連結して送ってください．\n'
                     .encode('utf-8'))
        conn.sendall('3回連続間違えるとゲームオーバーです．\n'.encode('utf-8'))
        conn.sendall('問題は"q:"で始まります．\n'.encode('utf-8'))
        conn.sendall('"q:"は除いて文字列処理をしてください．\n\n'.encode('utf-8'))
        conn.sendall('ex) q:dog,apple,lion\n'.encode('utf-8'))
        conn.sendall('上のような文字列が送られてきたら，下のような文字列をサーバーに送ります．\n'.encode('utf-8'))
        conn.sendall('appledoglion\n'.encode('utf-8'))
        conn.sendall('すべて正解すると，completeと送られてきます．\n'.encode('utf-8'))
        conn.sendall('--------------------------------------------\n\n'
                     .encode('utf-8'))

    def createAnswer(self, string):
        words = string.strip().split(',')
        words.sort()
        return ''.join(words)

    def mainProblem(self, conn):
        with open(ProblemThread.WORD_FILE, 'r') as f:
            for line in f:
                wrong = 0
                answer = self.createAnswer(line[2:])
                encoded = line.encode('utf-8')
                conn.sendall(encoded)

                while True:
                    data = conn.recv(1024)
                    if len(data) == 0:
                        break

                    if data.strip().decode('utf-8') == answer:
                        break
                    else:
                        wrong += 1
                        if wrong >= ProblemThread.WRONG_MAX:
                            conn.sendall('Game Over'.encode('utf-8'))
                            # TODO: maybe exists more better way. (don't use sys.exit())
                            sys.exit(0)
                        conn.sendall(encoded)

        conn.sendall('complete'.encode('utf-8'))
