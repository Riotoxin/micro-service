#!/usr/bin/env python
# coding: utf-8


import requests
from sqlalchemy import create_engine

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

db_uri = "postgres://postgres:lol123@localhost:5432/postgres"
engine = create_engine(db_uri)

engine.execute("""
    DROP TABLE IF EXISTS temperature
""")
engine.execute("""
    CREATE TABLE temperature(
    city text,
    time timestamp,
    temp float
)
""")

for key,values in weatherObj.weatherTemp.items():
    engine.execute("INSERT INTO temperature VALUES (%s, %s, %s)", (weatherObj.weatherCity['name'], key,weatherObj.weatherTemp[key]['temp']))
    

result_set = engine.execute("SELECT * FROM temperature")
for r in result_set:
    print(r)



