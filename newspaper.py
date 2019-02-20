import requests
from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-

"""
Created on Wed Feb 20 22:10:34 2019

@author: tomto
"""
print("蘋果熱門新聞")
dom=requests.get('https://tw.appledaily.com/hot/daily').text
soup=BeautifulSoup(dom,'html5lib')
for hot in soup.find('ul','all').find_all('li'):
    print(
            hot.find('div','aht_title_num').text,'|標題:',
            hot.find('div','aht_title').text,
            '|   觀看人數',hot.find('div','aht_pv_num').text
            )
print("-------------------")
print("自由即時新聞")
dom=requests.get('https://news.ltn.com.tw/list/breakingnews/all').text
soup=BeautifulSoup(dom,'html5lib')
for hot in soup.find('ul','list').find_all('li'):
    try:
        print("連結:","https:"+hot.a['href'])#在li底下，所以不必再找尋
        print("時間:",hot.find('a','tit').span.text.strip())#時間
        print("標題",hot.find('a','tit').p.text.strip())#新聞標題
        print("主題:",hot.find('div','tagarea').a.text.strip())#找尋新聞主題
        print("地區:",hot.find('div','tagarea').find_all('a')[1].text)#地區為a的第1個位置所以取1
        print("")
    except:
        print(" ")
