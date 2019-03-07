# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 21:11:01 2019

@author: tomto
"""

import googlemaps
from pprint import pprint

API_KEY=''
gmaps=googlemaps.Client(key=API_KEY)
geocode_result=gmaps.geocode("臺北市")
loc =geocode_result[0]['geometry']['location']
places=gmaps.places_radar(keyword="拉麵", location=loc, radius=20)['results']#(關鍵字,經緯度,範圍(公尺))
print("台北市半徑100公尺附近拉麵店數量:"+str(len(places)))
print("第一筆資料")
pprint(places[0])
