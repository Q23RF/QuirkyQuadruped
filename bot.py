import os
import time
import googleapiclient.discovery
from mastodon import Mastodon

mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space/'
)

def retrieve_new_videos():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCCBCiQ26pPnCcUV0S0QBGDq7E0R5_q2Cw"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        channelId="UC2e4Ukj5Pfr7cb3KpJAFBdQ",
        maxResults=10,
        order="date"
    )
    videos = request.execute()["items"]
    return videos

def compare_time(videos):
    for video in videos:
        publish_time = iso_to_struct(video["snippet"]["publishTime"])

def toot_update():
    txt=""
    mastodon.status_post(txt)

def iso_to_struct(iso):
    return time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")


def main():
    print(iso_to_struct("2023-02-18T03:00:09Z"))

if __name__ == "__main__":
    main()