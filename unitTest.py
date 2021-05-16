import requests
from sqlalchemy import create_engine

def test_weather_func(apiURI):
    weatherFunc(apiURI)
    db_uri1 = "postgres://postgres:lol123@localhost:5432/postgres"
    engine = create_engine(db_uri1)
    
    ret = engine.execute("SELECT count(*) FROM temperature")
    
    for r in ret:
        pass

    assert r[0] == 40
    
test_weather_func("http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=d76175a7e71fcaf018227f7c3af4106a")
