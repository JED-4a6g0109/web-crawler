# -*- coding: utf-8 -*-
import json
import re
import time
import requests
from bs4 import BeautifulSoup

tStart = time.time()#計時開始


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
    datelist=[]
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
    print ('今天有', len(articles), '篇文章')
    threshold = 10
    print ('熱門文章(> %d 推):' % (threshold))#推文篩選

    for a in articles:
        if int(a['push_count']) > threshold:
            datelist.append(a)
            print(a)
    print("大於",threshold,"推文有",len(datelist),"篇")
    print("json格式:")
    with open('gossiping.json', 'w', encoding='utf-8') as f:
        json.dump(datelist, f, indent=2, sort_keys=True, ensure_ascii=False)
        tEnd = time.time()#計時結束
print ('花費時間',tEnd - tStart,"秒")#原型長這樣


   
