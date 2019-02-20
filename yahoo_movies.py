# -*- coding: utf-8 -*-
import json
import re
import requests
from bs4 import BeautifulSoup
"""
Created on Sat Feb 16 21:58:01 2019

@author: tomto
"""

def get_web_page(url):
    resp = requests.get(
        url=url,
    )
    if resp.status_code != 200:
        return None
    else:
        return resp.text
    
def get_movie_id(url):
    try:
        movie_id=url.split('.html')[1].split('-')[-1]
    except:
        movie_id=url   

    return movie_id


def get_date(date_str):
    pattern='\d+-\d+-\d+'
    match=re.search(pattern,date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)
    
def get_movies(dom):
    soup = BeautifulSoup(dom,'html5lib')
    movies=[]#新增陣列存Dictionary
    rows=soup.find_all('div','release_info_text')
    for row in rows:
        movie=dict()#空的Dictionary
        movie['expectation'] = row.find('div','leveltext').span.text.strip()
        movie['ch_name']=row.find('div','release_movie_name').a.text.strip()
        movie['en_name']=row.find('div','release_movie_name').find('div','en').a.text.strip()
        movie['movie_id']=get_movie_id(row.find('div','release_movie_name').a['href'])#不能用release_foto原因是    rows=soup.find_all('div','release_info_text')指從release_info_text下手，而不是在他內部如果要跳出class用row.parent.find_previous_sibling poster_url的方法
        movie['poster_url']=row.parent.find_previous_sibling('div','release_foto').img['src']#previous_sibling用法 網址:https://blog.csdn.net/sunlizhen/article/details/73437102
        movie['release_date']=get_date(row.find('div','release_movie_time').text)
#replace
#str = "a a a a a";
#print (str.replace("a", "b",1))
#print (str.replace("a", "b",2))
#print (str.replace("a", "b",3))
#b a a a a
#b b a a a
#b b b a a
        movie['intro']=row.find('div','release_text').text.replace(u'\xa0', ' ').strip()#u/U:表示unicode字符串 ,\xa0為iso編碼不屬於unicode所以要剃除 網址:https://blog.csdn.net/IAlexanderI/article/details/79455027
        trailer_a=row.find_next_sibling('div','release_btn color_btnbox').find_all('a')[1]#next_sibling 應該是下一個類別 網址:https://blog.csdn.net/Winterto1990/article/details/47794941
        movie['trailer_url']=trailer_a['href'] if 'href' in trailer_a.attrs else'無預告片'
        movies.append(movie)
    return movies
    
#attrs
#可以搜尋指定屬性的值
#範例
#soup.find_all(attrs={"class": "sister"})
#[
#<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, 
#<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, 
#<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
#]

page = get_web_page('https://movies.yahoo.com.tw/movie_thisweek.html')
if page:
 
    movies=get_movies(page)
    for movie in movies:
        print(movies)
    with open('movie.json','w',encoding='utf-8') as f:
        json.dump(movies, f ,indent=2, sort_keys=True, ensure_ascii=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        