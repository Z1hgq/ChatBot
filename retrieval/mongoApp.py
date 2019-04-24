

# coding=utf-8

from flask import Flask, render_template, request, make_response
from flask import jsonify

from multiprocessing import Pipe, Process
import sys
import time  
import hashlib
import threading
import jieba
import datetime
import os

from main import top5results_emb
from main import clean_words
from main import cut_sentence
import random
import math
import gc
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

db = client['chatbot']
xhj_simple = db['xhj_simple']
xhj = db['xhj']
def heartbeat():
    print (time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()
timer = threading.Timer(60, heartbeat)
timer.start()
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]
def process1(conn):
    while True:
        obj = conn.recv()
        conn.send(top5results_emb(obj['req'],obj['q1'],obj['a1'],obj['v1']))
def process2(conn):
    while True:
        obj = conn.recv()
        conn.send(top5results_emb(obj['req'],obj['q2'],obj['a2'],obj['v2']))
def process3(conn):
    while True:
        obj = conn.recv()
        conn.send(top5results_emb(obj['req'],obj['q3'],obj['a3'],obj['v3']))
def process4(conn):
    while True:
        obj = conn.recv()
        conn.send(top5results_emb(obj['req'],obj['q4'],obj['a4'],obj['v4']))
try:  
    import xml.etree.cElementTree as ET  
except ImportError:  
    import xml.etree.ElementTree as ET


app = Flask(__name__,static_url_path="/static") 

@app.route('/message', methods=['POST'])
def reply():
    start_time = datetime.datetime.now()   
    req_msg = request.form['msg']
    print(cut_sentence(req_msg))
    questionList = []
    questionListVec = []
    answerList = []
    if cut_sentence(req_msg).rstrip(' \n') == '' or cut_sentence(req_msg).rstrip(' \n') == ' ':
        result = xhj_simple.find()
        for obj in result:
            questionList.append(obj['question'])
            answerList.append(obj['answer'])
            tmpLst = obj['vector'].rstrip(' \n').split(" ")
            questionListVec.append([float(x) for x in tmpLst])
    else:
        reg = ''
        for keyWord in list(set(cut_sentence(req_msg).split())):
            reg += '.*' + keyWord + '.*|'
        reg = reg[:-1]
        result = xhj.find({'question': {'$regex':reg}})
        for obj in result:
            questionList.append(obj['question'])
            answerList.append(obj['answer'])
            tmpLst = obj['vector'].rstrip(' \n').split(" ")
            questionListVec.append([float(x) for x in tmpLst])
    if len(questionList) >=4:
        q = chunks(questionList,4)
        a = chunks(answerList,4)
        v = chunks(questionListVec,4)
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
        # res_msg = cut_sentence(req_msg)
        # print(cut_sentence(req_msg).split())
        # print(list(set(cut_sentence(req_msg).split())))
        # return jsonify( { 'text': res_msg } )
        obj = {'req':req_msg,'q1':q1,'a1':a1,'v1':v1}
        parent_conn.send(obj)
        obj2 = {'req':req_msg,'q2':q2,'a2':a2,'v2':v2}
        parent_conn2.send(obj2)
        obj3 = {'req':req_msg,'q3':q3,'a3':a3,'v3':v3}
        parent_conn3.send(obj3)
        obj4 = {'req':req_msg,'q4':q4,'a4':a4,'v4':v4}
        parent_conn4.send(obj4)
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
                        if max_ < 0.9:
                            res_msg = '我没听懂你说什么惹'
                        print(res_msg)
                        if res_msg == ' ':
                            res_msg = '请与我聊聊天吧'
                        end_time = datetime.datetime.now() 
                        print('回复耗时:',end_time-start_time)  
                        return jsonify( { 'text': res_msg } )
    else:
        return jsonify( { 'text': '我没听懂你说什么惹' } )
@app.route("/")
def index(): 
    return render_template("index.html")
basedir = os.path.abspath(os.path.dirname(__file__))
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
    app.run(host = '0.0.0.0', port = 8808) 
