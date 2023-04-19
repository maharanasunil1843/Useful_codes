# import requests and BeautifulSoup libraries
import requests
from bs4 import BeautifulSoup

# define the URL of the YouTube channel
url = "https://www.youtube.com/@PythonSimplified"

# get the HTML content from the URL
response = requests.get(url)

# create a BeautifulSoup object from the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# find the meta tag that contains the channel ID
meta_tag = soup.find("meta", itemprop="channelId")

# get the content attribute of the meta tag
channel_id = meta_tag["content"]

# print the channel ID
print(channel_id)