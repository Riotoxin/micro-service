#!/usr/bin/env python
# coding: utf-8

import requests
import psycopg2
from psycopg2 import Error

weatherResponse = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=d76175a7e71fcaf018227f7c3af4106a")

if (weatherResponse.status_code == 200):
    print("Request was a Success")
else:
    print("Request failed with Code: ",weatherResponse.status_code)

weatherJson = weatherResponse.json()

class Weather:
    def __init__(self, weatherJson):
        self.weatherJson = weatherJson
        self.weatherTemp = {}
        self.timestamp = []
        i = 0
        
        self.weatherList = self.weatherJson['list']
        self.weatherCity = self.weatherJson['city']
        
        while(i < len(self.weatherList)):
            self.timestamp.append(self.weatherList[i]['dt_txt'])
            self.weatherTemp[self.weatherList[i]['dt_txt']] = self.weatherList[i]['main']
            i += 1

weatherObj =  Weather(weatherJson)

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=lol123")
cur = conn.cursor()
cur.execute("""
    DROP TABLE IF EXISTS temperature
""")
cur.execute("""
    CREATE TABLE temperature(
    city text,
    time timestamp,
    temp float
)
""")

for key,values in weatherObj.weatherTemp.items():
    cur.execute("INSERT INTO temperature VALUES (%s, %s, %s)", (weatherObj.weatherCity['name'], key,weatherObj.weatherTemp[key]['temp']))

conn.commit()



