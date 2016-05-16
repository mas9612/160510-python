#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import threading
import sqlite3
import random


class ProblemThread(threading.Thread):
    WRONG_MAX = 3
    WORD_FILE = 'words.txt'

    DB_FILE = 'word_data.db'
    WORD_COUNT_MAX = 234

    WORD_PER_ONE_PROBLEM = 10

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        random.seed()

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

    def mainProblem(self, conn):
        wrong = 0
        PROBLEM_AMOUNT = 100

        for i in range(PROBLEM_AMOUNT):
            words = 'q:' + self.fetchProblemWords()
            answer = self.createAnswer(words[2:])
            encoded = words.encode('utf-8')
            conn.sendall(encoded)

            while True:
                data = conn.recv(1024)
                if data.strip().decode('utf-8') == answer:  # correct answer
                    break
                else:
                    wrong += 1
                    if wrong >= ProblemThread.WRONG_MAX:
                        conn.sendall('Game Over'.encode('utf-8'))
                        print('Game over. Disconnected for', conn.getpeername())
                        conn.close()
                        return
                    conn.sendall(encoded)

        conn.sendall('complete'.encode('utf-8'))

    def fetchProblemWords(self):
        db_conn = sqlite3.connect(ProblemThread.DB_FILE)
        db_cursor = db_conn.cursor()

        query = 'select word from words order by random() limit 10'
        db_cursor.execute(query)
        words = db_cursor.fetchall()
        db_conn.close()

        ret_list = [w[0] for w in words]
        return ','.join(ret_list)

    def createAnswer(self, string):
        words = string.strip().split(',')
        words.sort()
        return ''.join(words)
