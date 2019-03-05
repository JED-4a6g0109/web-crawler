# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:57:43 2019

@author: tomto
"""
import re
import time
import requests
from bs4 import BeautifulSoup

def get_ip(dom):
    pattern='來自: \d+\.\d+\.\d+\.\d+'
    match=re.search(pattern,dom)
    if match:
        #print(match.group(0).replace('來自: ','')) 
        return match.group(0).replace('來自: ','')
        
    else:
        return None

API_KEY='a96e8d67886164f000eb76801242d5e5'
def get_country(ip):
    if ip:
        url='http://api.ipstack.com/{}?access_key={}'.format(ip,API_KEY)#format用{}來表示參數位置
        #print('bebug:',url)除錯確認url有沒有錯誤
        data=requests.get(url).json()#get ipstackAPI資訊轉成json
        #print(data) 取得dictionary
        country_name=data['country_name'] if data['country_name'] else None#存取判斷
        print('此篇作者國家:',country_name)#存取country_name
        return country_name
    return None

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
        if d.find('div', 'date').text.strip() == date:
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

current_page = get_web_page('https://www.ptt.cc/bbs/Gossiping/index.html')
if current_page:
    articles = []
    today = time.strftime("%m/%d").lstrip('0')
    current_articles,prev_url = get_articles(current_page, today)
    i=0
    while current_articles:#換頁
        articles += current_articles
        current_page = get_web_page('https://www.ptt.cc' + prev_url)
        current_articles, prev_url = get_articles(current_page, today)
        i+=1
        if i>4:
            break
    print('取得今日文章IP')
    country_to_count=dict()
    for article in articles[:100]:
        print('查詢IP:',article['title'])
        print('文章網址',article['href'])
        print()
        page=get_web_page(article['href'])#作者url
        if page:
            ip=get_ip(page)#取作者IP
            country=get_country(ip)#進API獲得dictionary轉成json再把country_name存入country
            if country in country_to_count.keys():#對應country_to_count假設已經有dictionary就累加
                #print(country_to_count.keys())dict()
                country_to_count[country]+=1
            else:
                country_to_count[country] =1
    print('各國ip分布')
    for k,v in country_to_count.items():
        print(k,v)
