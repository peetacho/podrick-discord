import requests
import json


class sendFact():
    def __init__(self):
        pass

        # Make the HTTP Api request
    def get_fact(self):

        url = 'https://uselessfacts.jsph.pl/random.json?language=en'

        response = requests.get(url)
        response_json = response.json()

        message_body = response_json["text"]

        return message_body
