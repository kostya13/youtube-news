import json
import os
import urllib.parse
import urllib.request
from config import CHAT_ID, TELEGRAM_TOKEN


def send(text):
    if os.getenv('TEST') == '1':
        print(text)
    else:
        api_url = "https://api.telegram.org/bot{0}/sendMessage".format(TELEGRAM_TOKEN)
        params = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'})
        try:
            with urllib.request.urlopen(api_url, params.encode()):
                pass
        except Exception as exc:
            print(f'Generated an exception: {exc}')


def save_db(db_name, db):
    with open(db_name, 'w', encoding='utf8') as dbfile:
        json.dump(db, dbfile, ensure_ascii=False, indent=2)


def load_db(db_name):
    try:
        with open(db_name, encoding='utf8') as dbfile:
            db = json.load(dbfile)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        db = {}
    return db


def load_url(url, uploads):
    with urllib.request.urlopen(url.format(uploads)) as response:
        return json.loads(response.read())