import os
from flask import Flask, request
from mastodon import Mastodon
import random
from pytube import Playlist
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
mastodon = Mastodon(access_token=os.environ['TOKEN'],
                    api_base_url='https://botsin.space/')

def get_random_vid(playlist_url):
    p = Playlist(playlist_url)
    urls = p.video_urls
    url = urls[random.randint(0, len(urls) - 1)]
    return url


playlist = "https://www.youtube.com/playlist?list=OLAK5uy_mhIfeEQekE1BSH2Qzwj-3AU-wTzIiC2Q4"


@app.route('/', methods=['HEAD', 'GET'])
def index():
    ua = request.headers.get('User-Agent')
    if ua == 'pipedream/1':
        url = get_random_vid(playlist)
        txt = "#推歌 #每日梯曲 #ATEEZ \n"
        mastodon.status_post(txt + url)
    return 'Hello!'


app.run(host='0.0.0.0', port=81)
