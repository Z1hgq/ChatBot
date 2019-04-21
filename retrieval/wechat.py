# coding=utf-8
import itchat
from multiprocessing import Pipe, Process
import time  
import threading
import datetime
from main import readFile
from main import top5results_emb
import random
import math
def heartbeat():
    print (time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()
timer = threading.Timer(60, heartbeat)
timer.start()
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
q = chunks(questionList,4)
a = chunks(answerList,4)
v = chunks(vectorValueList,4)
questionList = []
answerList = []
vectorValueList = []
q1 = q[0]
a1 = a[0]
v1 = v[0]
q2 = q[1]
a2 = a[1]
v2 = v[1]
q3 = q[2]
a3 = a[2]
v3 = v[2]
q4 = q[3]
a4 = a[3]
v4 = v[3]
q = []
a = []
v = []
def process1(conn):
    while True:
        req = conn.recv()
        conn.send(top5results_emb(req,q2,a2,v2))
def process2(conn):
    while True:
        req = conn.recv()
        conn.send(top5results_emb(req,q1,a1,v1))
def process3(conn):
    while True:
        req = conn.recv()
        conn.send(top5results_emb(req,q3,a3,v3))
def process4(conn):
    while True:
        req = conn.recv()
        conn.send(top5results_emb(req,q4,a4,v4))
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    start_time = datetime.datetime.now()   
    req_msg = msg.text
    res_msg = '^_^'
    parent_conn.send(req_msg)
    parent_conn2.send(req_msg)
    parent_conn3.send(req_msg)
    parent_conn4.send(req_msg)
    res = []
    while True:
        res1 = parent_conn.recv()
        print(res1)
        print('res1')
        res.append(res1[2])
        while True:
            res2 = parent_conn2.recv()
            print(res2)
            print('res2')
            res.append(res2[2])
            while True:
                res3 = parent_conn3.recv()
                print(res3)
                print('res3')
                res.append(res3[2])
                while True:
                    res4 = parent_conn4.recv()
                    print(res4)
                    print('res4')
                    res.append(res4[2])         
                    max_ = max(res)
                    if res1[2] == max_:                        
                        res_msg =res1[1]
                    if res2[2] == max_:                        
                        res_msg =res2[1]
                    if res3[2] == max_:                        
                        res_msg =res3[1]
                    if res4[2] == max_:                        
                        res_msg =res4[1] 
                    # if res1[2] > res2[2]:
                    #     res_msg = res1[1]
                    # else:
                    #     res_msg = res2[1]
                    print(res_msg)
            # res_msg = get_response(req_msg)
            # 如果接受到的内容为空，则给出相应的恢复
                    if res_msg == ' ':
                        res_msg = '请与我聊聊天吧'
                    end_time = datetime.datetime.now() 
                    print('回复耗时:',end_time-start_time)  
                    return res_msg


# 启动APP
if (__name__ == "__main__"): 
    parent_conn, child_conn = Pipe()
    parent_conn2, child_conn2 = Pipe()
    parent_conn3, child_conn3 = Pipe()
    parent_conn4, child_conn4 = Pipe()
    p = Process(target=process1, args=(child_conn,))
    p.start()
    p2 = Process(target=process2, args=(child_conn2,))
    p2.start()
    p3 = Process(target=process3, args=(child_conn3,))
    p3.start()
    p4 = Process(target=process4, args=(child_conn4,))
    p4.start()
    itchat.auto_login(hotReload=True,enableCmdQR=2)
    itchat.run()