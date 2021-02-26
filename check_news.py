import json
from html.parser import HTMLParser

import requests

from config import NEWS_FILE, SUBSCRIPTION_FILE
from common import send, save_db, load_db


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if 'var ytInitialData = ' in data:
            self.text = data[20:-1]


def parse(url, title):
    #print('--', title)
    page = requests.get(url)
    content = page.text
    parser = MyHTMLParser()
    parser.feed(content)
    jsn = json.loads(parser.text)
    messages = []
    for e in jsn['contents']['twoColumnBrowseResultsRenderer']['tabs']:
        try:
            for c in (e['tabRenderer']['content']['sectionListRenderer']['contents']):
                for cc in c['itemSectionRenderer']['contents']:
                    postId = cc['backstagePostThreadRenderer']['post']['backstagePostRenderer']['postId']
                    lines = []
                    #print(cc['backstagePostThreadRenderer']['post']['backstagePostRenderer']['publishedTimeText']['runs'][0]['text'])
                    for t in (cc['backstagePostThreadRenderer']['post']['backstagePostRenderer']['contentText']['runs']):
                        lines.append(t['text'])
                    messages.append((postId, '\n'.join(lines)))
                    if len(messages) == 3:
                        return messages
        except Exception as e:
            pass
    return messages


fmt = 'https://www.youtube.com/channel/{}/community'
videos = load_db(SUBSCRIPTION_FILE)
posts =  load_db(NEWS_FILE)

for k in videos.keys():
    url = fmt.format(k)
    title = videos[k]['title']
    messages = parse(url, title)
    if messages:
        mk = posts.setdefault(k, None)
        for m in messages:
            if m[0] != mk:
                url = fmt.format(k)
                text  = "[{}]({})\n{}".format(title, url, m[1])
                send(text)
            else:
                break
        posts[k] = messages[0][0]
save_db(NEWS_FILE, posts)
