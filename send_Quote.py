import requests
import json

url = "http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en"


class sendQuote():

    def get_quote(self):
        try:
            response = requests.get(url).json()

            author = ""
            if response["quoteAuthor"] == "":
                author = "Anonymous"
            else:
                author = response["quoteAuthor"]

            message_body = "{} ~{}".format(
                response["quoteText"], author.strip())

            return message_body
        except:
            response = requests.get(url).json()

            author = ""
            if response["quoteAuthor"] == "":
                author = "Anonymous"
            else:
                author = response["quoteAuthor"]

            message_body = "{} ~{}".format(
                response["quoteText"], author.strip())

            return message_body
