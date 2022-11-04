import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def weather_forecast_for_location(city_name):
    # city_name = "Rybnik"
    limit = 3
    api = os.environ.get('weather_api')
    try:
        location = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api}')
        loc_json = location.json()
        lon = loc_json[1]['lon']
        lat = loc_json[1]['lat']
        weather_forecast = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api}&units=metric')
        forecast_json = weather_forecast.json()
        forecast_dict = dict(forecast_json)
        return forecast_dict
    except Exception as e:
        print(e)
        print("there was an error")
        return "error"


def date_conversion(date):
    new_date = date.replace("-", " ").replace(":", " ")
    split_date = new_date.split()
    datetime_obj = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), int(split_date[3]))
    new_date_format = datetime_obj.strftime('%B %d %I %p')
    return new_date_format


def three_day_forecast(city_name):
    forecast = weather_forecast_for_location(city_name)
    current_day = int(forecast['list'][0]['dt_txt'][8:-9])
    day_one = []
    day_two = []
    day_three = []
    day_four = []
    forecasts = [day_one, day_two, day_three, day_four]

    for i in range(len(forecast['list'])):
        if int(forecast['list'][i]['dt_txt'][8:-9]) in range(current_day, current_day+4):
            date = forecast['list'][i]['dt_txt']

            if int(date[11:-6]) in range(9, 20, 3):
                if int(date[8:-9]) == current_day:
                    if len(day_one) == 0:
                        day_one.append(f"Today {date_conversion(date)}")
                    else:
                        day_one.append(f"At {date_conversion(date)[-5:]}")
                    day_one.append(f"Temperature: {round(forecast['list'][i]['main']['temp'])} degrees")
                    day_one.append(f"Weather: {forecast['list'][i]['weather'][0]['description']}")
                    day_one.append(f"Pressure: {forecast['list'][i]['main']['pressure']} hPa")
                elif int(forecast['list'][i]['dt_txt'][8:-9]) == (current_day + 1):
                    if len(day_two) == 0:
                        day_two.append(f"Tomorrow, {date_conversion(date)}")
                    else:
                        day_two.append(f"At {date_conversion(date)[-5:]}")
                    day_two.append(f"Temperature: {round(forecast['list'][i]['main']['temp'])} degrees")
                    day_two.append(f"Weather: {forecast['list'][i]['weather'][0]['description']}")
                    day_two.append(f"Pressure: {forecast['list'][i]['main']['pressure']} hPa")
                elif int(forecast['list'][i]['dt_txt'][8:-9]) == (current_day + 2):
                    if len(day_three) == 0:
                        day_three.append(f"On {date_conversion(date)}")
                    else:
                        day_three.append(f"At {date_conversion(date)[-5:]}")
                    day_three.append(f"Temperature: {round(forecast['list'][i]['main']['temp'])} degrees")
                    day_three.append(f"Weather: {forecast['list'][i]['weather'][0]['description']}")
                    day_three.append(f"Pressure: {forecast['list'][i]['main']['pressure']} hPa")
                elif int(forecast['list'][i]['dt_txt'][8:-9]) == (current_day + 3):
                    if len(day_four) == 0:
                        day_four.append(f"On {date_conversion(date)}")
                    else:
                        day_four.append(f"At {date_conversion(date)[-5:]}")
                    day_four.append(f"Temperature: {round(forecast['list'][i]['main']['temp'])} degrees")
                    day_four.append(f"Weather: {forecast['list'][i]['weather'][0]['description']}")
                    day_four.append(f"Pressure: {forecast['list'][i]['main']['pressure']} hPa")
                else:
                    pass
    return forecasts
