import requests
import database as db
from datetime import datetime , timedelta
import time
API_Key = "YOUR API SHOULD BE HERE"
#================================================================
def cooardintaes(city):
    city = city.lower()
    cities = {"london" : (51.50, -0.12),
              "tehran" : (35.68,51.38)
              }
    return cities.get(city)
#================================================================
def retry(func):
    def wrapper(*args , **kwargs):
        attempt = 3
        for i in range(attempt):
            try:
                return func(*args , **kwargs)
            except requests.ConnectionError:
                wait = 2**i    
                print(f"Connection failed. Retrying in {wait} seconds...")
                time.sleep(wait)
                if i == attempt - 1:
                    return {"error" : "after 3 attempts, connection fails"}
    return wrapper
#================================================================
@retry
def get_weather(city):
    print("Ran from the begigining.....")
    city = city.lower()
    check_cache = db.chech_cache(city)
    coardinate = cooardintaes(city)
    
    if coardinate == None:
       print("coor nadari") 
       return f"You have to insert the latitude and longitude of city name {city}"
    if check_cache == None:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={coardinate[0]}&lon={coardinate[1]}&exclude=hourly,daily&appid={API_Key}"
        response = requests.get(url)
        data = response.json()
        temperature = data["main"]["temp"]
        humidity= data["main"]["humidity"]
        description = data["weather"][0]["description"]
        cached_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        db.add_weather(city , temperature , humidity, description,cached_at)
        print("ezafe be database")
        return ((city, temperature ,humidity, description, cached_at) )
    
    current = datetime.now()
    print("current:" , current)
    cache_time = datetime.strptime(check_cache[4],"%d/%m/%Y, %H:%M:%S")
    print("cache time: ",cache_time)
    print("current - cache time:",current - cache_time)
    if current - cache_time >= timedelta(minutes=1):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={coardinate[0]}&lon={coardinate[1]}&exclude=hourly,daily&appid={API_Key}"
        response = requests.get(url)
        data = response.json()
        temperature = data["main"]["temp"]
        humidity= data["main"]["humidity"]
        description = data["weather"][0]["description"]
        cached_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        db.update_cache_weather(city, temperature ,humidity, description, cached_at)
        print("update database")
        return (city, temperature ,humidity, description, cached_at)
    print("Az cache")
    return check_cache
#========================================================




print(get_weather("TehraN"))



