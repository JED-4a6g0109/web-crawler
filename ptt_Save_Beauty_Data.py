# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 21:09:45 2019

@author: tomto
"""

import requests
import re
import os
import json
import time
from bs4 import BeautifulSoup
import urllib.request


tStart = time.time()#計時開始

def parse(dom):
    soup=BeautifulSoup(dom,'lxml')
    links=soup.find(id='main-content').find_all('a')
    img_urls=[]
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com',link['href']):
            img_urls.append(link['href'])
    return img_urls

#圖片網址樣式 
#http://i.imgur.com/cQRXBZr.jpg
#http://i.imgur.com/cQRXBZr
#https://i.imgur.com/cQRXBZr.jpg
#http://imgur.com/cQRXBZr.jpg    
#https://imgur.com/cQRXBZr.jpg
#https://imgur.com/cQRXBZr
#http://m.imgur.com/cQRXBZr.jpg
#https://m.imgur.com/cQRXBZr.jpg
#http(s)//(i)(m)或沒有.......(.jpg),正規表示 'https?://(i.)?(m.)?imgur.com'
#24行加r是串內容為原始字串,撰寫字串不需要跳脫特殊字元


def save(img_urls,title):
    if img_urls:
        try:
            dname=title.strip()
            os.makedirs(dname)#os.makedirs(path[, mode]) 建立資料夾名稱為dname
            for img_url in img_urls:
                if img_url.split('//')[1].startswith('m'):
                    img_url=img_url.replace('//m.' '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url=img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url+='.jpg'
                fname=img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname,fname))#os.path.join(資料夾名稱,檔案名稱) 
        except Exception as e:
            print(e)
#檔名裡不能有\/:*?"<>| 所以titile有這些特殊字元無法創檔案
#47 http://imgur.com/A2wmlqW.jpg.split('//')
#           >['http:',imgur.com/A2wmlqW.jpg]
#47、49、51有效下載網址需要i.與結尾.jpg
#53 URL 简单分割:
##!/usr/bin/python3
#url = "http://www.baidu.com/python/image/123456.jpg"
##以“.” 进行分隔
#path =url.split(".")
#print(path)
#以上输出结果：我们在学习 python 爬虫的时候例如需要保存图片，图片名称的获取，可以依照下列方法：

#['http://www', 'baidu', 'com/python/image/123456', 'jpg']
#以 / 进行分隔：
#
#['http:', '', 'www.baidu.com', 'python', 'image', '123456.jpg']
            
#我们在学习 python 爬虫的时候例如需要保存图片，图片名称的获取，可以依照下列方法：
#
#path =url.split("/")[-1]
#输出结果：
#'123456.jpg'    
            
#54 網址:https://blog.csdn.net/NKFCP114/article/details/7957011
#urllib.request.urlretrieve用法 網址https://blog.csdn.net/pursuit_zhangyu/article/details/80556275

            


def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print ('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'lxml')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']
    match=re.search('\d+.\d',prev_url)
    print("正在抓取第"+match.group()+"頁...")
    articles = []

    divs = soup.find_all('div', 'r-ent')
    for d in divs:
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10
            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div', 'author').text if d.find('div', 'author') else ''

                articles.append({
                    'title': title,
                    'href': 'https://www.ptt.cc'+href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_url

current_page = get_web_page('https://www.ptt.cc/bbs/Beauty/index.html')
if current_page:
    articles = []
    date=time.strftime("%m/%d").lstrip('0')
    current_articles,prev_url = get_articles(current_page, date)
    i=0
    while current_articles:#換頁
        articles += current_articles
        current_page = get_web_page('https://www.ptt.cc' + prev_url)
        current_articles, prev_url = get_articles(current_page, date)
        i+=1
        if i>40:
            break
    for article in articles:
       print ('processing',article)
       page = get_web_page(article['href'])
       if page:
           img_urls=parse(page)#取得全部照片網址
           save(img_urls,article['title'])#處理網址格式與下載
           article['num_image']=len(img_urls)#照片總數
           print( article['num_image'])

        
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)#儲存成json
tEnd = time.time()#計時結束
print ('花費時間',tEnd - tStart,"秒")#原型長這樣
