#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import urllib2
import time
import urllib
import json
import hashlib
import base64
import urllib.request
import urllib.parse
 
 
def xfstt(wav):
    f = open(wav, 'rb')  #rb表示二进制格式只读打开文件
    file_content = f.read()
    # file_content 是二进制内容，bytes类型
    # 由于Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。
    # 如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes
    # 以Unicode表示的str通过encode()方法可以编码为指定的bytes
    base64_audio = base64.b64encode(file_content)   #base64.b64encode()参数是bytes类型，返回也是bytes类型
    body = urllib.parse.urlencode({'audio': base64_audio})
 
    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'bf7290edfbff63eff178d0247c6c89c8'
    param = {"engine_type": "sms16k", "aue": "raw"}
 
    x_appid = '5cbc07b9'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8')) #改('''')
    # 这是3.x的用法，因为3.x中字符都为unicode编码，而b64encode函数的参数为byte类型，
    # 所以必须先转码为utf-8的bytes
    x_param = str(x_param, 'utf-8')
 
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5((api_key + str(x_time) + x_param).encode('utf-8')).hexdigest() #改
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    # 不要忘记url = ??, data = ??, headers = ??, method = ?? 中的“ = ”，这是python3
    req = urllib.request.Request(url = url, data = body.encode('utf-8'), headers = x_header, method = 'POST')
    result = urllib.request.urlopen(req)
    result = result.read().decode('utf-8')
    print(result)
    return result
 