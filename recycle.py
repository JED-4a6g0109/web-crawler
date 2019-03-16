# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:20:13 2019

@author: tomto
"""

import requests
import json
from bs4 import BeautifulSoup

i=int(1)#從第一頁開始
items=[]
while (i<25):#最多為24頁
    i=str(i)#轉成url字串
    url = 'http://recycle.epb.taichung.gov.tw/recying/resource.asp?Page='+i
    result = requests.get(url, timeout=30)
    result.encoding='big5'#增加encoding=‘big5’，解決中文亂碼問題
    soup = BeautifulSoup(result.text, 'lxml')
    rows=soup.find('div','context_main_box').find_all('tr')[3].find_all('td')[5].find_all('tr')
    for row in rows:
        item=list()  
        
    #舊原碼        item.append('物品:'+row.find('font').text)#物品
    #        item.append(row.find_all('font')[2].text)#是否可回收
    #        if row.find_all('font')[3].text:
    #            item.append(row.find_all('font')[3].text)
    #        else:
    #            item.append('無說明')
    #        items.append(item)
        
        #原先是list所以建立dictionary在輸出成json會比較整齊
        if row.find('font').text =='物品中文名稱':#因為21行不能從[1]開始爬所以用if來把('tr')[0]給剃除
            print('不需要的資料')
        else:
            item=row.find('font').text#物品
            for img in row.find_all('a'):#圖片，找到所有('a')後找尋['href'] 備註:他會是一個個tr往下搜，所以這個for迴圈在tr[位置]底下的td搜尋
                img=img['href'].replace('../..','http://recycle.epb.taichung.gov.tw')#取得資料會是../../files，所以把../..取代就行了，根據全部圖片開頭都是以http://recycle.epb.taichung.gov.tw
                image=img 
            recycle=row.find_all('font')[2].text#是否可回收
            if row.find_all('font')[3].text:#備註有的為空所以要塞選掉
                remark=row.find_all('font')[3].text
            else:
                remark='無說明'
            #轉成dicionary方便弄成json
            items.append({
                    'item':item,
                    'image':image,
                    'recycle':recycle,
                    'remark':remark
                    })
    i=int(i)#轉成int因為前面while需要int判別
    i=i+1#遞增頁數
    for item in items:
            print(item)#輸出資料確保無誤
            
#輸出json
with open('recycle.json','w',encoding='utf-8') as f:
    json.dump(items,f,indent=2,sort_keys=True,ensure_ascii=False)
    
    
    
    #舊原碼    print('物品',row.find('font').text)#物品
    #    if row.find_all('font')[1].text:
    #        print('英文名稱:',row.find_all('font')[1].text)#td去搜會發現一個問題，list[0]會為空導致錯誤，所以用font來爬
    #        #網址:https://blog.csdn.net/pddddd/article/details/47110813
    #    else:
    #        print('英文名稱:'+'無')
    #    print('是否可回收:',row.find_all('font')[2].text)#是否可回收
    #    print('說明:',row.find_all('font')[3].text)#說明
    #    print()
    #        print(row.find('img',{'src':re.compile('\.jpg')}))



    



