#!python3
#coding:utf-8
import json, sys, requests
 
def getWeather(weatherPlace):
    weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % (weatherPlace)
    response = requests.get(weatherJsonUrl)
    try:
        response.raise_for_status()
    except:
        print("网址请求出错")
        
    #将json文件格式导入成python的格式
    weatherData = json.loads(response.text)
    
    #以好看的形式打印字典与列表表格
    #import pprint
    #pprint.pprint(weatherData)
    
    w = weatherData['data']
    
    #日期
    date_a = []
    #最高温与最低温
    highTemp = []
    lowTemp = []
    #天气
    weather = []
    #进行五天的天气遍历
    res = "地点：%s" % w['city'] + '\n'
    for i in range(len(w['forecast'])):
        date_a.append(w['forecast'][i]['date'])
        highTemp.append(w['forecast'][i]['high'])
        lowTemp.append(w['forecast'][i]['low'])
        weather.append(w['forecast'][i]['type'])
        
        #输出
        res += "日期：" + date_a[i]
        res += "\t温度：最" + lowTemp[i] + '℃~最' + highTemp[i] + '℃\n'
        res += "\t天气：" + weather[i] +'\n\n'
    res += "\n今日着装：" + w['ganmao'] + '\n'
    res += "当前温度：" + w['wendu'] + "℃"
    print(res)
    return res