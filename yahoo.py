# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 21:58:01 2019

@author: tomto
"""

def get_movie_id(url):
    try:
        movie_id=url.split('.html')[1].split('-')[-1]
        print(movie_id)

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
    movies=[]
    rows=soup.find.all('div','release_info_text')
    for row in rows:
        movie=dict()