

# coding=utf-8

from flask import Flask, render_template, request, make_response
from flask import jsonify

import sys
import time  
import hashlib
import threading
import jieba
import datetime
import os
from flask_cors import CORS
from main import readFile
from main import top5results_emb
import random
def heartbeat():
    print (time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()
start = datetime.datetime.now()
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
end = datetime.datetime.now()
print('时间:',end-start)
def get_response(req):
    return top5results_emb(req,questionList,answerList,vectorValueList)
try:  
    import xml.etree.cElementTree as ET  
except ImportError:  
    import xml.etree.ElementTree as ET


import re
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])
app = Flask(__name__,static_url_path="/static") 
CORS(app,resources=r'/*')
def create_uuid(self): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/message', methods=['POST'])

def reply():   
    req_msg = request.form['msg']
    res_msg = '^_^'
    res_msg = get_response(req_msg)
    # 如果接受到的内容为空，则给出相应的恢复
    if res_msg == ' ':
      res_msg = '请与我聊聊天吧'

    return jsonify( { 'text': res_msg } )

@app.route("/")
def index(): 
    return render_template("index.html")
basedir = os.path.abspath(os.path.dirname(__file__))
 
@app.route('/up_photo', methods=['post'])
def up_photo():
    img = request.files.get('photo')
    path = basedir+"/static/photo/"
    file_path = path+img.filename
    img.save(file_path)
    return jsonify({'file_path':file_path,'file_name':img.filename})
#

'''
初始化seq2seqModel，并进行动作

    1. 调用执行器的主程序
    2. 生成一个在线decode进程，来提供在线聊天服务
'''
#_________________________________________________________________
#_________________________________________________________________

# 启动APP
if (__name__ == "__main__"): 
    app.run(host = '0.0.0.0', port = 8808) 
