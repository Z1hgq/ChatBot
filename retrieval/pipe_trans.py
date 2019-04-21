# -*- coding:utf-8 -*-
import multiprocessing
from multiprocessing import Pipe, Process
import time
from main import readFile
from main import top5results_emb
import math
import sys
import datetime
questionListPath = './data/questionList'
answerListPath = './data/answerList'
questionListVecPath = './data/questionListVec'
questionList = readFile(questionListPath)
answerList = readFile(answerListPath)
vectorValueList = []
with open(questionListVecPath) as f:
    for line in f.readlines():
        tmpLst = line.rstrip(' \n').split(" ")
        vectorValueList.append([float(x) for x in tmpLst])
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]
result = []
q = chunks(questionList,2)
a = chunks(answerList,2)
v = chunks(vectorValueList,2)
questionList = []
answerList = []
vectorValueList = []
q1 = q[0]
a1 = a[0]
v1 = v[0]
q2 = q[1]
a2 = a[1]
v2 = v[1]
q = []
a = []
v = []


def test(conn):
    while True:
        req = conn.recv()
        conn.send(top5results_emb(req,q2,a2,v2))
def test2(conn):
    while True:
        req = conn.recv()
        conn.send(top5results_emb(req,q1,a1,v1))

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    parent_conn2, child_conn2 = Pipe()
    p = Process(target=test, args=(child_conn,))
    p.start()
    p2 = Process(target=test2, args=(child_conn2,))
    p2.start()
    while True:
        sys.stdout.write("> ")
        sys.stdout.flush()
        req = sys.stdin.readline()
        s = datetime.datetime.now()
        parent_conn.send(req)
        parent_conn2.send(req)
        print (parent_conn.recv()) 
        print (parent_conn2.recv())  
        e = datetime.datetime.now()
        print(e-s)
