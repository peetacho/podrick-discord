import requests
import json


class sendWeather():
    def __init__(self):
        pass

        # Make the HTTP Api request
    def get_weather(self):

        url = 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=en'

        response = requests.get(url)
        response_json = response.json()

        forecast_desc = response_json["forecastDesc"]
        outlook = response_json["outlook"]

        message_body = forecast_desc + " " + outlook

        return message_body
