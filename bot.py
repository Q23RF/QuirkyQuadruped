import os
import time
import googleapiclient.discovery
from mastodon import Mastodon
from dotenv import load_dotenv

load_dotenv()
epoch_sec = 10800 #checks every three hour
channel_id = "UC2e4Ukj5Pfr7cb3KpJAFBdQ"

mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space/'
)

def retrieve_videos():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=10,
        order="date"
    )
    videos = request.execute()["items"]
    return videos

def compare_time(now, videos):
    new_videos = []
    for video in videos:
        publish_time = iso_to_sec(video["snippet"]["publishTime"]) #this seems to be UTC?
        if now - publish_time < epoch_sec:
            new_videos.append(video)
    return new_videos


def toot_update(videos):
    for video in videos:
        iso_time = video["snippet"]["publishTime"]
        publish_time = iso_time[0:10] + " " + iso_time[11:19] + " UTC"
        title = video["snippet"]["title"]
        v_id = video["id"]["videoId"]
        url = "https://www.youtube.com/watch?v=" + v_id
        txt=f"{publish_time} YouTube(@ATEEZofficial) update\n{title}\n{url}"
        mastodon.status_post(txt)

def iso_to_struct(iso):
    return time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")

def iso_to_sec(iso):
    return time.mktime(time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ"))


def main():
    videos = retrieve_videos()
    new_videos = compare_time(time.time(), videos)
    toot_update(new_videos)

if __name__ == "__main__":
    main()