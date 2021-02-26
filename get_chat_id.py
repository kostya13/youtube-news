#!/bin/env python3
import json
import urllib.request

from config import TELEGRAM_TOKEN

url = "https://api.telegram.org/bot{0}/getUpdates?timeout=3".format(TELEGRAM_TOKEN)
with urllib.request.urlopen(url) as response:
    response_json = json.loads(response.read())
    print(response_json['result'][0]['message']['chat']['id'])