import requests
import json
from datetime import datetime
import numpy as np  

def get_weather_html(city: str, api_key: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    response = requests.get(url)
    data = json.loads(response.text)

    # Получаем данные о погоде
    polarday=False
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    wind_deg = data['wind']['deg']
    precipitation_type =data["rain"]["1h"] if "rain" in data else "нет данных"
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
    if sunrise==sunset: polarday=True
    description = data['weather'][0]['description']
    dew_point = calculate_dew_point(temperature, humidity)

    # Формируем HTML-страницу
    html = f"""
    <html>
        <head>
            <title>Погода в городе {city}</title>
        </head>
        <body>
            <h1>Погода в городе {city}</h1>
            Температура: {temperature}°C</br>
            Влажность: {humidity}%</br>
            Точка росы: {dew_point}°C</br>
            Описание: {description}</br>
            Объем осадков за последний час (мм): {precipitation_type}</br>
            Направление ветра: {get_wind_direction(wind_deg)}</br>
            Скорость ветра: {wind_speed} м/с</br>
            """
    if polarday:
        html+="Полярный день</br>"
    else:
        html+="""
            Восход солнца: {sunrise}</br>
            Заход солнца: {sunset}</br>
            """
    html+=f"""
        </body>
    </html>
    """

    return html

def calculate_dew_point(temperature: float, humidity: float) -> float:
    a = 17.27
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + \
            (np.log(humidity / 100.0))
    dew_point = (b * alpha) / (a - alpha)
    return round(dew_point, 1)

def get_wind_direction(deg: float) -> str:
    directions = ['северный', 'северо-восточный', 'восточный', 'юго-восточный',
                  'южный', 'юго-западный', 'западный', 'северо-западный']
    index = round(deg / (360.0 / len(directions))) % len(directions)
    return directions[index]