import time
from posixpath import split
from googleapiclient.discovery import build
import json
from os import system, rename

GoogleApiKey = 'AIzaSyAY19lM15PP3yvmPgZlsZQA0-t8i6pogmE'

youtube = build('youtube', 'v3', developerKey=GoogleApiKey)

# Get Video ID from user
videoID = input("Enter video ID: ")
videoLink = "https://youtu.be/" + videoID

if videoID.startswith('https://www.youtube.com/watch?v='):
    videoID = videoID.replace('https://www.youtube.com/watch?v=', '')
elif videoID.startswith('https://youtu.be/'):
    videoID = videoID.replace('https://youtu.be/', '')

request = youtube.videos().list(part=['snippet', 'statistics'],id=videoID)
# UCKpfgyqNLeubc86Yt2pxKSA
response = request.execute()

json_data = json.dumps(response, indent=4)

json_response = json.loads(json_data)

system('clear')
title = json_response["items"][0]["snippet"]["title"]
channelTitle = json_response["items"][0]["snippet"]["channelTitle"]
print("Video Title...\n" + title)
print("\nChannel...\n" + channelTitle)

system("youtube-dl \""+ videoLink + "\" --write-info-json --skip-download")

fileName = title+"-"+videoID+".info.json"

rename(fileName, "youTubeVideoData.json")
fileName = "youTubeVideoData.json"
file = open(fileName, "r")
for i in file:
    video_json_data = json.loads(i)

video_json_dump = json.dumps(video_json_data, indent=4)

for i in range(len(video_json_data["formats"])):
    video_height = video_json_data["formats"][i]["height"]
    video_width = video_json_data["formats"][i]["width"]
    video_format = video_json_data["formats"][i]["format"]
    video_ext = video_json_data["formats"][i]["ext"]
    if "audio only" in video_format:
        print("\nAudio Only")
        continue
    format_id = video_json_data["formats"][i]["format_id"]
    format_note = video_json_data["formats"][i]["format_note"]
    print(str(i+1) + ". (" + format_id + ") " + format_note + " " + video_ext)