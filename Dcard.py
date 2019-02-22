# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 21:26:45 2019

@author: tomto
"""
import requests
import re
from bs4 import BeautifulSoup

resp=requests.get('https://www.dcard.tw/f')
soup=BeautifulSoup(resp.text,'html.parser')
articles=[]
for div in soup.find_all('div',re.compile('PostEntry_content_\w{6}')):#re用法 網址:http://www.runoob.com/python3/python3-reg-expressions.html
    articles.append({
            'title':div.h3.text.strip(),
            'excerpt':div.find_all('div')[0].text.strip(),#摘要為PostEntry_content_g2afgv的陣列0
            'likecount':re.findall(r'\d+', div.find_all('div')[1].text.strip())[0],#讚數在第二個div所以要給[1],在第[0]然後只取數字div:PostEntry_reactions_3bbr43
            'respones':re.findall(r'\d+',div.find_all('div')[1].text.strip())[1],#與讚數在同個div底下位於第[1]的位置div:PostEntry_comments_2iY8V3
            'href':div.parent.parent['href']#PostEntry_wrapper_s_0ZLi第一個父節點,PostEntry_root_V6g0rd為第二個節點       
            })
    
    print('共%d篇'% (len(articles)))
    for a in articles:
        print(a)
