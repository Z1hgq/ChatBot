#! /usr/bin/python
# coding = utf-8

# ToDo: get weather info from weather.com.cn
# Author: Steven
# Date: 2013/05/13

import urllib.request
import json

# get weather html and parse to json
weatherHtml = urllib.request.urlopen('http://m.weather.com.cn/data/101010100.html').read()
weatherJSON = json.JSONDecoder().decode(weatherHtml)
weatherInfo = weatherJSON['weatherinfo']

# print weather info
print ('城市：\t', weatherInfo['city'])
print ('时间：\t', weatherInfo['date_y'])
print ('24小时天气：')
print ('温度：\t', weatherInfo['temp1'])
print ('天气：\t', weatherInfo['weather1'])
print ('风速：\t', weatherInfo['wind1'])
print ('紫外线：\t', weatherInfo['index_uv'])
print ('穿衣指数：\t', weatherInfo['index_d'])
print ('48小时天气：')
print ('温度：\t', weatherInfo['temp2'])
print ('天气：\t', weatherInfo['weather2'])
print ('风速：\t', weatherInfo['wind2'])
print ('紫外线：\t', weatherInfo['index48_uv'])
print ('穿衣指数：\t', weatherInfo['index48_d'])
print ('72小时天气：')
print ('温度：\t', weatherInfo['temp3'])
print ('天气：\t', weatherInfo['weather3'])
print ('风速：\t', weatherInfo['wind3'])