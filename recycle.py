# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:20:13 2019

@author: tomto
"""

import requests
import json
from bs4 import BeautifulSoup


url = 'http://recycle.epb.taichung.gov.tw/recying/resource.asp'
result = requests.get(url, timeout=30)
result.encoding='big5'#增加encoding=‘big5’，解決中文亂碼問題
soup = BeautifulSoup(result.text, 'lxml')
rows=soup.find('div','context_main_box').find_all('tr')[3].find_all('td')[5].find_all('tr')
items=list()
for row in rows:
    item=list()
    item.append(row.find('font').text)
    item.append(row.find_all('font')[2].text)
    if row.find_all('font')[3].text:
        item.append(row.find_all('font')[3].text)
    else:
        item.append('無說明')
    items.append(item)
    
print('回收資料')
for item in items:
    print(item)
with open('recycle.json','w',encoding='utf-8') as f:
    json.dump(items,f,indent=2,sort_keys=True,ensure_ascii=False)
#    print('物品',row.find('font').text)#物品
#    if row.find_all('font')[1].text:
#        print('英文名稱:',row.find_all('font')[1].text)#td去搜會發現一個問題，list[0]會為空導致錯誤，所以用font來爬
#        #網址:https://blog.csdn.net/pddddd/article/details/47110813
#    else:
#        print('英文名稱:'+'無')
#    print('是否可回收:',row.find_all('font')[2].text)#是否可回收
#    print('說明:',row.find_all('font')[3].text)#說明
#    print()
#        print(row.find('img',{'src':re.compile('\.jpg')}))



    



