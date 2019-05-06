# -*- coding:utf-8 -*-

'''
1、python版本 python3.6
'''
import requests
import urllib.request
import re

#获取每一个主页面中的分类条目url链接
def get_page(num):
    html = requests.get("http://www.doutula.com/article/list/?page=)"+str(num)).text
    reg = '<a href="(.*?)" class="list-group-item'
    urls = re.findall(reg, html)
    return urls

#获取分类条目中每个图片的url链接
def get_pic(urls):
    html = requests.get(urls).text
    reg = '<img src="(.*?)" alt'
    urls = re.findall(reg, html, re.S)
    return urls

#下载图片
n=1
for x in range(2):
    print("正在下载第{}页......".format(x+1))
    for i in get_page(x):
        for j in get_pic(i):
            pic_file = "img/"+str(n)+".jpg"
            urllib.request.urlretrieve(j, pic_file)
            n = n + 1
print("下载完成，共下载{}张图片".format(n-1))