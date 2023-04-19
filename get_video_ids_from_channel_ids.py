#Extracting data from Multipe Channels
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from googleapiclient.discovery import build
from pprint import pprint

api_key = "AIzaSyBSc-oK77V2wne1evfRYa5zSBD0GAIc-7Q"
channel_ids = ['UC8butISFwT-Wl7EV0hUK0BQ', #1. Free Code Camp
               'UCbV60AGIHKz2xIGvbk0LLvg', #2. Jay Shetty
               'UCcYzLCs3zrQIBVHYA1sK2sw', #3. Sadhguru
               'UCHnyfMqiRRG1u-2MsSQLbXA', #4. Varitasium
               'UCLLw7jmFsvfIVaUFsLs8mlQ', #5. Luke Barousse
               'UCnz-ZXXER4jOvuED5trXfEA', #6. Tech TFQ
               'UCiT9RITQ9PW6BhXK0y2jaeg', #7. Ken Jee
               'UC7cs8q-gJRlGwj4A8OmCmXg', #8. Alex The Analyst
               'UC2UXDak6o7rBm23k3Vv5dww', #9. Tina Huang
               'UCAuUUnT6oDeKwE6v1NGQxug' #10. Ted Talks
               ]

youtube = build('youtube', 'v3', developerKey=api_key)

#Step 1: Function to get channel stastics
def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)) #joining all the values of the list 'channel_ids' with a ',' separation.
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(channel_name=response['items'][i]['snippet']['title'], #fetches all the channel name
                    views=response['items'][i]['statistics']['viewCount'], #fetches total views of the channel
                    subscribers=response['items'][i]['statistics']['subscriberCount'], #fetches total subscribers of the channel
                    total_videos=response['items'][i]['statistics']['videoCount'], #fetches total no of videos in a channel
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'] #fetches the playlist id of the channel
                    )
        all_data.append(data)

    return all_data #return a dictionary of the data

#pprint(get_channel_stats(youtube,channel_ids))

channel_stastics = get_channel_stats(youtube,channel_ids) #gives a json format data (dict in dict)
channel_data = pd.DataFrame(channel_stastics) #putting all the dict data into a dataframe
print(channel_data)

print(channel_data.dtypes) #initially all the data are in object type
channel_data['subscribers'] = pd.to_numeric(channel_data['subscribers'])
channel_data['views'] = pd.to_numeric(channel_data['views'])
channel_data['total_videos'] = pd.to_numeric(channel_data['total_videos'])
print(channel_data.dtypes) #now the datatype of the above features has been changed to int64.

#ax1 = sns.barplot(x='channel_name', y='subscribers', data=channel_data)
#ax2 = sns.barplot(x='channel_name', y='views', data=channel_data)
#ax3 = sns.barplot(x='channel_name', y='total_videos', data=channel_data)
#plt.show()

#Extracting playlist_id of a single entity from the dataframe channel_data
playlist_id = channel_data.loc[channel_data['channel_name'] == "Ken Jee", 'playlist_id'].iloc[0]
print(playlist_id, type(playlist_id))

#Setp 2: Function to get video ids of a channel through its playlistId. Youtube allows to fetch max. 50 ids only.
def get_video_ids(youtube, playlist_id):

    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults = 50)
    response = request.execute()

    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

#till this point youtube has allowed to fetch only 50 video ids. But through following logic, remaining video ids can be fetched.
    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids

video_ids = get_video_ids(youtube, playlist_id)
print(len(video_ids))

#Setp 3: Function to get video details using the video ids of a playlistID.
def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50): #passing it in for loop to remove the limitation of 50 video details
        request = youtube.videos().list(
            part = 'snippet,statistics',
            id=','.join(video_ids[i:i+50])) #since youtube has limit of 50 data limit.

        response = request.execute()

        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               Total_comments = video['statistics']['commentCount'])
            all_video_stats.append(video_stats)

    return all_video_stats

video_details = get_video_details(youtube, video_ids)

#Passing data into a dataframe
video_data = pd.DataFrame(video_details)
print(video_data.dtypes) #this shows that initially all the datas are in object format.

video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Total_comments'] = pd.to_numeric(video_data['Total_comments'])
print(video_data.dtypes)
print(video_data)
#video_data.to_csv("C:\\Users\\ADMIN\\Desktop\\video_data.csv", index= False)

top10_videos = video_data.sort_values(by="Views", ascending= False).head(10)
#print(top10_videos)

#ax1 = sns.barplot(x = "Views", y = "Title", data= top10_videos)
#plt.show()

#adding month to check upload frequency of video monthwise
video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')
print(video_data)

videos_per_month = video_data.groupby('Month', as_index= False).size() #converting the output into a dataframe
print(videos_per_month)

#ax2 = sns.barplot(x="Month", y="size", data = videos_per_month)
#plt.show()