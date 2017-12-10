# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
from PIL import Image
import time
import re
import os

if os.path.exists('D:\\photo\\'):
    print("图片储存目录存在\n")
else:
    os.mkdir('D:\\photo\\')
    print("已创建图片储存目录！\n")
print('欢迎来到西电查询系统(请输入你想执行的操作前面的数字)：\n1.校园网流量\n2.天气查询\n')
choice = input()
if choice == '1':
    session = requests.session()
    username = input("输入你的学号：")
    password = input("输入你的密码：")
    postdata = {'LoginForm[username]': username,
                'LoginForm[password]': password}
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    headers = {
        "Host": "10.255.44.1:8800",
        "Referer": r"http://10.255.44.1:8800/",
        'User-Agent': agent
    }
    url_login = 'http://10.255.44.1:8800/'


    def get_captcha():
        t = str(int(time.time() * 1000))
        captcha_url = 'http://10.255.44.1:8800/site/captcha?refresh=1&_=' + t
        r = session.get(captcha_url, headers=headers)
        tem = r.json()['url']
        captcha_url = 'http://10.255.44.1:8800' + tem
        r = session.get(captcha_url, headers=headers)
        
        with open('D:\\photo\\captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()

        try:
            im = Image.open('D:\\photo\\captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("请输入打开的图片上的数字\n>")
        return captcha



    def get_csrf():
        index_url = 'http://10.255.44.1:8800/'
        index_page = session.get(index_url, headers=headers)
        html = index_page.text
        pattern = r'name="_csrf" value="(.*?)"'
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]


    postdata['_csrf']=get_csrf()
    postdata['LoginForm[verifyCode]']=get_captcha()
    result = session.post(url_login,data=postdata,headers=headers)
    soup_2 = BeautifulSoup(result.text, 'lxml')
    have_used = soup_2.select('#w3-container > table > tbody > tr')
    if len(have_used) == 0:
        print("请检查输入是否错误!")
    for used in have_used:
        cell = [i.text for i in used.find_all('td')]
        print("已用流量:"+cell[1]+"\n"+"剩余流量:"+cell[2]+"\n"+"套餐外:"+cell[3])

if choice == '2':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    url = 'http://tianqi.2345.com/today-57036.htm'
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    weather_1 = soup.select('#skInfo > div.filter > ul')
    weather_2 = soup.select('#wrap > div.hour-detail.today-detail > div.tbody > div.time-main > dl.day > dd > ul > li.ord1 > span.phrase')
    for weather2 in weather_2:
        print(weather2.get_text(),'\n')
    for weather1 in weather_1:
         print(weather1.get_text(),'\n')
    print('可能缺失部分数据，请谅解.')
