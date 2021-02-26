#!/usr/bin/env python3
import concurrent.futures
from datetime import datetime

from config import GOOGLE_API_KEY, MYCHANNEL_ID, SUBSCRIPTION_FILE
from common import send, save_db, load_db, load_url

TIME_FMT = '%Y-%m-%dT%H:%M:%S'
maxResult = 50
threads = 20
base_url = 'https://youtube.googleapis.com/youtube/v3/'

subscriptions_url = f'{base_url}subscriptions?part=snippet&channelId={{}}&maxResults={maxResult}&key={GOOGLE_API_KEY}'
playlist_url = f'{base_url}playlistItems?part=snippet&playlistId={{}}&key={GOOGLE_API_KEY}'


channels_db = load_db(SUBSCRIPTION_FILE)

jsn = load_url(subscriptions_url, MYCHANNEL_ID)
nextPageToken = f"&pageToken={jsn['nextPageToken']}"
total = jsn["pageInfo"]["totalResults"]
subscriptions = jsn['items']
while len(subscriptions) < total:
    jsn = load_url(subscriptions_url + nextPageToken, MYCHANNEL_ID)
    subscriptions += jsn['items']

recieved_channel_id = [s['snippet']['resourceId']['channelId'] for s in subscriptions]
recieved_dict = dict(zip(recieved_channel_id, subscriptions))

to_update = set(recieved_channel_id) - set(channels_db.keys())
to_delete = set(channels_db.keys()) - set(recieved_channel_id)

for key in to_delete:
    del channels_db[key]

for k in to_update:
    snippet = recieved_dict[k]['snippet']
    channelId = snippet['resourceId']['channelId']
    uploads = 'UU{}'.format(channelId[2:])
    print(snippet['title'], snippet['channelId'], uploads)
    channels_db[channelId] = {
        'title': snippet['title'],
        'uploads': uploads,
        'last': "1970-01-01T00:00:00"}

with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    futures = (executor.submit(load_url, playlist_url, channels_db[k]['uploads']) for k in channels_db)
    for future in concurrent.futures.as_completed(futures):
        try:
            jsn = future.result()
            for j in reversed(jsn['items']):
                snip = j['snippet']
                title = snip['title']
                published = snip['publishedAt'][:-1]
                channelId = snip['channelId']
                channel_name = snip['channelTitle']
                video_url = 'https://youtu.be/{}'.format(snip['resourceId']['videoId'])
                if (datetime.strptime(published, TIME_FMT) >
                    datetime.strptime(channels_db[channelId]['last'], TIME_FMT)):
                    channels_db[channelId]['last'] = published
                    #print(title, published, f'{channel_name}\n{video_url}')
                    send(f'{channel_name}\n{video_url}')
        except Exception as exc:
            print(f'Generated an exception: {exc}')

save_db(SUBSCRIPTION_FILE, channels_db)
