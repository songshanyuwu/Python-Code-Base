# -*- coding:utf-8 -*-
#original author: 
# 这是从两个作者那里摘抄合并过来的
# 此版本为命令行界面
#
# python             3.7.3
# requests           2.22.0
# bs4                0.0.1
# urllib3            1.25.3
# pypinyin           0.35.4
# 

import requests
import urllib.request
import bs4
import re
# 因为两个网站一个查询城市的value是汉字，另一个是拼音，所以要导入pypinyin模块
# 暂时没有更优雅的解决方案，除了换查询网站
import pypinyin
from PIL import ImageTk as itk

# 获取天气信息
def tianqiforecast(city):
    # city = input('请输入所要查询天气的城市：')
    url = 'http://toy1.weather.com.cn/search?cityname=' + city + '&callback=success_jsonpCallback&_=1548048506469'
    #print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Cookie': '__guid=182823328.3322839646442213000.1543932524694.901; vjuids=1858d43b6.167798cbdb7.0.8c4d7463d5c5d; vjlast=1543932526.1543932526.30; userNewsPort0=1; f_city=%E5%B9%B3%E9%A1%B6%E5%B1%B1%7C101180501%7C; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1543932526,1543932551,1543932579; Wa_lvt_1=1547464114,1547464115,1547880054,1547983123; defaultCty=101181001; defaultCtyName=%u5546%u4E18; monitor_count=6; Wa_lpvt_1=1547983809'}
    response = requests.get(url, headers = headers)
    #获得成功返回的json格式(success_jsonpCallback)
    success_jsonpCallback = response.content.decode('utf-8')
    #print(success_jsonpCallback)
    
    #判断是否有城市编号
    citys = re.findall('"ref":"(.*?)~.*?~(.*?)~.*?~(.*?)~.*?~.*?~.*?~.*?~(.*?)"', success_jsonpCallback, re.S)
    if (len(citys) == 0):
        print('未查找到该城市')
        exit(-5)
    #显示输出所有节点
    #for i in range(0, len(citys)):
        #print(i + 1, ':%14s%14s%16s%16s ' % (citys[i][0], citys[i][3], citys[i][2], citys[i][1]))
        #print(i + 1, '{:>14},{:>14},{:>18},{:>18}'.format(citys[i][0], citys[i][3], citys[i][2], citys[i][1]))

    #choose = int(input('请选择城市编号：[1~' + str(len(citys)) + ']\n'))
    choose=1
    #len(citys[choose - 1][0] 长度为9:城市主节点；
    if (len(citys[choose - 1][0]) == 9):
        if (citys[choose - 1][0][0] != '1' or citys[choose - 1][0][1] != '0' or citys[choose - 1][0][2] != '1'):
            print('暂时无法查询国外天气,程序已退出')
            exit(404)
        else:
            url2 = 'http://www.weather.com.cn/weathern/' + citys[choose - 1][0] + '.shtml'

        responseweather = requests.get(url2, headers=headers)
        html2 = responseweather.content.decode('utf-8')
        
        # 通过正则提取有用的数据
        weather = re.findall('<li class="date-.*?".*?".*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)
        weather.append(re.findall(
            '<p class="weather-in.*?" title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">(.*?)</p>',
            html2, re.S))
        
        Hightempture = re.findall( '<script>var eventDay =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)
        
        Lowtempture = re.findall( 'var eventNight =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)
        
        print("*"*20+'查询城市为：'+ str(citys[choose - 1][3])+'    '+str(citys[choose - 1][1])+"*"*20)
        print('日期   星期     天气    最低温  最高温    风向        风力变化        风向')
        
        # 通过循环输出天气信息
        for i in range(0, 8):
            #      此处是format， > 是代表右对齐
            print('{:>3} {:>4} {:>6} {:>6} {:>6} {:>10} {:>14} {:>10}'.format(weather[i][0],weather[i][1],weather[8][i][0],Lowtempture[0][i],Hightempture[0][i],weather[8][i][1],weather[8][i][3],weather[8][i][2]))
            
    #len(citys[choose - 1][0] 长度为12:城市的子节点；
    # 话说我在调试和学习中，这段代码就没运行过，-_-||
    if (len(citys[choose - 1][0]) == 12):
        url2 = 'http://forecast.weather.com.cn/town/weathern/' + citys[choose - 1][0] + '.shtml'
        responseweather = requests.get(url2, headers=headers)
        html2 = responseweather.content.decode('utf-8')

        weather = re.findall('<li class="date-.*?".*?"da.*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)

        html2 = re.sub('lt;', '<', html2)
        
        weather.append(re.findall('<p class="weather-in.*?" title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">\\r\\n(.*?)\\r\\n',  html2, re.S))

        Hightempture = re.findall('var eventDay = \["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)

        Lowtempture = re.findall('var eventNight = \["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];',  html2, re.S)
        
        b='查询城市为：'+str(citys[choose - 1][3])+'   '+str( citys[choose - 1][2])+ '    ' +str(citys[choose - 1][1])
        print(b)

        print(weather)
        for i in range(0, 8):
            print('{:>3} {:>4} {:>4} {:>10} {:>10} {:>10} {:>14} {:>10}'.format(weather[i][0],weather[i][1],weather[8][i][0],Lowtempture[0][i],Hightempture[0][i],weather[8][i][1],weather[8][i][3],weather[8][i][2]))



# 获取PM2.5的信息
def getPM25(searchcity):
    #将城市转为拼音
    scity = ''
    for i in pypinyin.pinyin(searchcity, style=pypinyin.NORMAL):
        scity += ''.join(i)
    
    site = 'http://www.pm25.com/city/' + scity + '.html'
    html = urllib.request.urlopen(site)
    soup =bs4.BeautifulSoup(html,"html.parser")
    # 城市名称
    city = soup.find("span",{"class":"city_name"})
    # AQI指数
    aqi = soup.find("a",{"class":"cbol_aqi_num"})
    # pm25指数
    pm25 = soup.find("span",{"class":"cbol_nongdu_num_1"})
    # pm25指数单位
    pm25danwei = soup.find("span",{"class":"cbol_nongdu_num_2"})
    # 空气质量等级
    quality = soup.find("span",{"class":re.compile('cbor_gauge_level\d$')})
    # 空气质量描述
    result = soup.find("div",{"class":'cbor_tips'})
    
    replacechar = re.compile("<.*?>")  #为了将<>全部替换成空
    space = re.compile(" ")
    
    #输出结果
    print("*"*20+"今日  " + city.string + "  PM2.5查询结果"+"*"*20)
    print(u'AQI指数：' + aqi.string)
    print(u'PM2.5浓度：' + pm25.string + pm25danwei.string)
    print(u'空气质量：' + quality.string)
    print(str(space.sub("",replacechar.sub('',str(result))).encode('utf-8'),'utf-8').replace('\n', ''))
    print("*"*65)




if __name__=='__main__':
    city = input('请输入所要查询天气的城市：')
    cityPinyin = ''
    for i in pypinyin.pinyin(city, style=pypinyin.NORMAL):
        cityPinyin += ''.join(i)
    getPM25(cityPinyin)
    tianqiforecast(city)
