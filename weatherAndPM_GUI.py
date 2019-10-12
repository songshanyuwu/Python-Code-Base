# -*- coding:utf-8 -*-
#original author:
# 这是从两个作者那里摘抄合并过来的
# 此版本为GUI界面，使用的是Tkinter
#
# python             3.7.3
# requests           2.22.0
# bs4                0.0.1
# urllib3            1.25.3



from tkinter import *
import tkinter as tk
import requests
from PIL import ImageTk as itk
import urllib.request
from time import ctime
import bs4    #besutifulsoup的第三版
import re
import pypinyin


class MyFrame(Frame):
    def __init__(self):
        self.root=Tk()
 
        self.root.title("天气查询")
        self.root.geometry('760x500+200+120')
        
        # 因为没有设置背景图片，所以注释
        #bg = tk.Canvas(self.root, width=740, height=480, bg='white')
        #self.img = itk.PhotoImage(file="bg.gif")
        #bg.place(x=10, y=10)
        #bg.create_image(0, 0, anchor=NW, image=self.img)
 
        self.city = Entry(self.root, width=16, font=("仿宋", 18, "normal"))
        self.city.place(x=150, y=20)
 
        citylabel=Label(self.root,text='查询城市',font=("仿宋", 18, "normal"))
        citylabel.place(x=20,y=20)
        #查询天气按钮
        chaxun = Button(self.root, width=10, height=1, text="查询天气", bg='#00CCFF', bd=3, font="bold")
        chaxun.bind("<Button-1>", self.search)
        chaxun.place(x=380, y=20)
        #显示天气框
        self.result=Listbox(self.root,heigh=23,width=90,font=("仿宋", 12, "normal"))
        self.result.place(x=20,y=60)
 
    def tianqiforecast(self,searchcity):
        #print('请输入所要查询天气的城市：')
        city = searchcity
        # city='jinan'
        url = 'http://toy1.weather.com.cn/search?cityname=' + city + '&callback=success_jsonpCallback&_=1548048506469'
        #print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Cookie': '__guid=182823328.3322839646442213000.1543932524694.901; vjuids=1858d43b6.167798cbdb7.0.8c4d7463d5c5d; vjlast=1543932526.1543932526.30; userNewsPort0=1; f_city=%E5%B9%B3%E9%A1%B6%E5%B1%B1%7C101180501%7C; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1543932526,1543932551,1543932579; Wa_lvt_1=1547464114,1547464115,1547880054,1547983123; defaultCty=101181001; defaultCtyName=%u5546%u4E18; monitor_count=6; Wa_lpvt_1=1547983809'
}
        response = requests.get(url, headers=headers)
        html1 = response.content.decode('utf-8')

        citys = re.findall('"ref":"(.*?)~.*?~(.*?)~.*?~(.*?)~.*?~.*?~.*?~.*?~(.*?)"', html1, re.S)
        if (len(citys) == 0):
            print('未查找到该城市')
            exit(-5)
        #for i in range(0, len(citys)):
        #    print(i + 1, ':%14s%14s%14s%14s ' % (citys[0], citys[3], citys[2], citys[1]))
        #choose = int(input('请选择城市编号：[1~' + str(len(citys)) + ']\n'))
        choose=1
        if (len(citys[choose - 1][0]) == 9):
            if (citys[choose - 1][0][0] != '1' or citys[choose - 1][0][1] != '0' or citys[choose - 1][0][2] != '1'):
                print('暂时无法查询国外天气,程序已退出')
                exit(404)
            else:
                url2 = 'http://www.weather.com.cn/weathern/' + citys[choose - 1][0] + '.shtml'
            responseweather = requests.get(url2, headers=headers)
            html2 = responseweather.content.decode('utf-8')
            weather = re.findall('<li class="date-.*?".*?".*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)
            weather.append(re.findall(
                '<p class="weather-in.*?" title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">(.*?)</p>',
                html2, re.S))
            Hightempture = re.findall(
                '<script>var eventDay =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2,
                re.S)
            Lowtempture = re.findall(
                'var eventNight =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];',
                html2, re.S)
            
            b='查询城市为：'+ str(citys[choose - 1][3])+'    '+str(citys[choose - 1][1])
            self.result.insert(END, b)
            c='日期   星期     天气      最低温  最高温    风向        风力变化        风向'
            self.result.insert(END, c)
            # 通过循环输出天气信息
            for i in range(0, 8):
                #      此处是format， > 是代表右对齐
                a = '{:>3} {:>4} {:<14} {:<6} {:<6} {:>10} {:>14} {:>10}'.format(weather[i][0],weather[i][1],weather[8][i][0],Lowtempture[0][i],Hightempture[0][i],weather[8][i][1],weather[8][i][3],weather[8][i][2])
                self.result.insert(END, a)

        if (len(citys[choose - 1][0]) == 12):
            url2 = 'http://forecast.weather.com.cn/town/weathern/' + citys[choose - 1][0] + '.shtml'
            responseweather = requests.get(url2, headers=headers)
            html2 = responseweather.content.decode('utf-8')
            weather = re.findall('<li class="date-.*?".*?"da.*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)
            html2 = re.sub('lt;', '<', html2)
            weather.append(re.findall(
                '<p class="weather-in.*?" title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">\\r\\n(.*?)\\r\\n',
                html2, re.S))
            Hightempture = re.findall(
                'var eventDay = \["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)
            Lowtempture = re.findall(
                'var eventNight = \["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];',
                html2, re.S)
            
            b='查询城市为：'+str(citys[choose - 1][3])+'   '+str( citys[choose - 1][2])+ '    ' +str(citys[choose - 1][1])
            self.result.insert(0,b)
            # 通过循环输出天气信息
            for i in range(0, 8):
                a = '{:>3} {:>4} {:>4} {:>10} {:>10} {:>10} {:>14} {:>10}'.format(weather[i][0],weather[i][1],weather[8][i][0],Lowtempture[0][i],Hightempture[0][i],weather[8][i][1],weather[8][i][3],weather[8][i][2])
                self.result.insert(END, a)


    def search(self,event):
        mycity=self.city.get()
        if(mycity!=''):
            self.result.delete(0,END)
            self.city.delete(0,END)
            self.tianqiforecast(mycity)
            self.getPM25(mycity)
            
    def getPM25(self,searchcity):
        #将城市转为拼音
        scity = ''
        for i in pypinyin.pinyin(searchcity, style=pypinyin.NORMAL):
            scity += ''.join(i)
        
        site = 'http://www.pm25.com/city/' + scity + '.html'
        html = urllib.request.urlopen(site)
        #soup =bs4.BeautifulSoup(html)
        soup =bs4.BeautifulSoup(html,"html.parser")
        
        city = soup.find("span",{"class":"city_name"})  # 城市名称
        aqi = soup.find("a",{"class":"cbol_aqi_num"})   # AQI指数
        pm25 = soup.find("span",{"class":"cbol_nongdu_num_1"})   # pm25指数
        pm25danwei = soup.find("span",{"class":"cbol_nongdu_num_2"})   # pm25指数单位
        quality = soup.find("span",{"class":re.compile('cbor_gauge_level\d$')})  # 空气质量等级
        result = soup.find("div",{"class":'cbor_tips'})   # 空气质量描述
        replacechar = re.compile("<.*?>")  #为了将<>全部替换成空
        space = re.compile(" ")
        
        d = "*"*20+"今日PM2.5查询结果"+"*"*20
        self.result.insert(END, d)
        e = u'\nAQI指数：' + str(aqi.string)
        self.result.insert(END, e)
        f = u'\nPM2.5浓度：' + str(pm25.string) + str(pm25danwei.string)
        self.result.insert(END, f)
        g = u'\n空气质量：' + str(quality.string)
        self.result.insert(END, g)
        h = str(space.sub("",replacechar.sub('',str(result))).encode('utf-8'),'utf-8')
        self.result.insert(END, h)
        
 
if __name__=='__main__':
    myframe=MyFrame()
    myframe.root.mainloop()
