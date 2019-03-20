# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 22:56:18 2019

@author: tomto
"""
import requests
import csv
from bs4 import BeautifulSoup
import codecs

query='ps4主機'
items=list()#其實可以不用設items但為了可讀性與變數方便存入csv，所以還是把item再丟進items會比較整齊
next_page='?&p=1'#頁碼

while(next_page!='javascript: void(0)'):#從取得下一次判斷式可以明確是否爬到最後一頁，如果到最會一頁24行會設定為javascript: void(0)這時直接列印全部items
    page=requests.get('https://ezprice.com.tw/s/'+query+next_page).text#get
    soup=BeautifulSoup(page,'html5lib')
    
    for div in soup.find_all('div','pagination clearfix'):#取得下一頁
        
        if div.find('li','next').a['href'] != 'javascript: void(0)':#如果沒有下一次他的text會是javascript: void(0)所以直接寫if
            
            print(div.find('li','next').a['href'])
            next_page=div.find('li','next').a['href']
            print('目前的next_page:',next_page)
            
        else:#如果是javascript: void(0)把next_page設為javascript: void(0)
            next_page='javascript: void(0)'
            
    for div in soup.find_all('div','search-rst clearfix'):
        
        item=list()
        item.append(div.h2.a.text.strip())#物品
        
    #    item.append(div.p.span.text.strip())#支付方式
    #    print(div.p.text.strip())
        
        price=div.find('span','num').text#價錢
        item.append(price)
        
        if div.find('span','platform-name'):#賣場
            
            item.append(div.find('span','platform-name').text.strip())
        
        else:
            
            item.append('無')
            print('無')
            
        item.append(div.find('a')['href'])#賣場網址
        print(item)
        items.append(item)
        
#列印全部items
print('共%d項商品' % (len(items)))
for item in items:
    print(item)
    
##編碼設為utf-8
#寫入csv
#https://segmentfault.com/q/1010000002493464
with codecs.open('ya.csv','w','utf_8_sig')as f:
    writer=csv.writer(f)
    writer.writerow(('品項','價格','商家','賣場網址'))
    for item in items:
        writer.writerow((column for column in item))
    
#無編碼寫入csv
#with open('ezpricedata1.csv','w',encoding='utf-8',newline='') as f:
#    writer=csv.writer(f)
#    writer.writerow(('品項','價格','商家','賣場網址'))
#    for item in items:
#        writer.writerow((column for column in item))