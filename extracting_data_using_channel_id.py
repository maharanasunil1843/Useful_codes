#Extracting Data from one channel
#Ted Talks : UCAuUUnT6oDeKwE6v1NGQxug

import pandas as pd
import seaborn as sns
from googleapiclient.discovery import build

api_key = "AIzaSyBSc-oK77V2wne1evfRYa5zSBD0GAIc-7Q"
channel_id = "UCAuUUnT6oDeKwE6v1NGQxug" #Ted Talks Channel Id

youtube = build('youtube', 'v3', developerKey=api_key)

#Function to get channel stastics
def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id)
    response = request.execute()

    data = dict(channel_name=response['items'][0]['snippet']['title'],
                views=response['items'][0]['statistics']['viewCount'],
                subscribers=response['items'][0]['statistics']['subscriberCount'],
                total_videos=response['items'][0]['statistics']['videoCount'])

    return data

print(get_channel_stats(youtube,channel_id))

