# -*- coding: UTF-8 -*-
import requests
import itchat
import json
from itchat.content import *
import os
from pydub import AudioSegment
from kedaxunfei import xfstt

def get_response_tuling(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : '3c4f1aa741314038a324f424634c19bd',
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

def asr(msg):
    #语音消息识别转文字输出
    msg['Text'](msg['FileName'])
    path = './' + str(msg['FileName'])
    print(path)
    song = AudioSegment.from_mp3(path)
    song.export("tmp.wav", format="wav")
    os.remove(msg['FileName'])
    return 'speech'
    # return xfstt('tmp.wav')

@itchat.msg_register(TEXT)#因为之前把itchat.content全部import了，里面有TEXT变量
def tuling_reply_text(msg):
    # 注册文字消息获取后的处理
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received a: ' + msg['Text']
    return get_response_tuling(msg['Text']) or defaultReply

@itchat.msg_register(RECORDING)
def tuling_reply(msg):
    # 注册语音消息获取后的处理
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received a: ' + msg['Type']

    # 如果图灵Key出现问题，那么reply将会是None
    # print(msg)
    asrMessage = asr(msg)
    return get_response_tuling(asrMessage) or defaultReply
    # return defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动hotReload=True
itchat.auto_login(hotReload=True)
itchat.run()