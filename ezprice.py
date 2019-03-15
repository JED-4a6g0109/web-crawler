# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 22:56:18 2019

@author: tomto
"""
import requests
from bs4 import BeautifulSoup
query='ps4主機'
page=requests.get('https://ezprice.com.tw/s/'+query).text
soup=BeautifulSoup(page,'html5lib')
items=list()
for div in soup.find_all('div','search-rst clearfix'):
    item=list()
    item.append(div.h2.a.text.strip())
    item.append(div.p.span.text.strip())

    price=div.find('span','num').text
    item.append(price)
    if div.find('span','platform-name'):
        item.append(div.find('span','platform-name').text.strip())
    else:
        item.append('無')
    items.append(item)
print('共%d項商品' % (len(items)))
for item in items:
    print(item)