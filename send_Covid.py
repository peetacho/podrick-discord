import requests
import json

url = "https://api.covid19api.com/country/china"


class sendCovid():

    def __init__(self):
        self.hk_stats_yesterday = []
        self.hk_stats_today = []

    def get_hk_stats(self):
        payload = {}
        headers = {}

        response = requests.request(
            "GET", url, headers=headers, data=payload).json()

        hk_stats = [d for d in response if d['Province'] == 'Hong Kong']
        self.hk_stats_yesterday = hk_stats[-2]
        self.hk_stats_today = hk_stats[-1]

        message_body = "There are {} confirmed cases, {} deaths, and {} active today.".format(
            self.subtract("Confirmed"),
            self.subtract("Deaths"),
            self.subtract("Active"))

        return message_body

    def subtract(self, status):
        if(status == "Active"):
            return self.hk_stats_yesterday[status] - self.hk_stats_today[status]
        else:
            return self.hk_stats_today[status] - self.hk_stats_yesterday[status]
