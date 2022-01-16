# Script to download YouTube videos using youtube-dl

import os
import youtube_dl
import json
from googleapiclient.discovery import build

# Clear Screen for any previous output
os.system('clear')

# YouTube API Key
from dotenv import load_dotenv
load_dotenv()
youTubeApiKey = os.getenv("youTubeApiKey")

# Take youtube video ID from user
videoId = str(input("Enter video ID or URL: "))
if videoId.startswith('https://www.youtube.com/watch?v='):
    videoId = videoId.replace('https://www.youtube.com/watch?v=', '')
elif videoId.startswith('https://youtu.be/'):
    videoId = videoId.replace('https://youtu.be/', '')
# else:
#     print("Invalid URL")
#     print("Exiting...")
#     exit()
videoId = 'fD7LIqkKisc'

# Build YouTube API service
youTube = build('youtube', 'v3', developerKey=youTubeApiKey)
# Get video info - statistics and snippets(title, channel title etc.)
youTubeVideoRequest = youTube.videos().list(part='snippet, statistics', id=videoId)
youTubeVideoResponse = youTubeVideoRequest.execute()
# Convert to JSON
youTubeVideoResponse = json.dumps(youTubeVideoResponse, indent=4)
# Load JSON to a dictionary
youTubeVideoResponse = json.loads(youTubeVideoResponse)

# Get video info
videoTitle = youTubeVideoResponse["items"][0]["snippet"]["title"]
videoChannelTitle = youTubeVideoResponse["items"][0]["snippet"]["channelTitle"]
videoViewCount = youTubeVideoResponse["items"][0]["statistics"]["viewCount"]
videoLikeCount = youTubeVideoResponse["items"][0]["statistics"]["likeCount"]
videoCommentCount = youTubeVideoResponse["items"][0]["statistics"]["commentCount"]

# Print video info to user
os.system('clear')
print("Video Title: " + videoTitle)
print("Channel: " + videoChannelTitle)

# Call youtube-dl to get video info
os.system('youtube-dl --write-info-json --skip-download "' + videoId + '"')

# rename file from youtube-dl to youTubeVideoData.json
fileName = videoTitle + "-" + videoId + ".info.json"
os.rename(fileName, "youTubeVideoData.json")

# Read data from youTubeVideoData.json file
json_file = open('youTubeVideoData.json')
for i in json_file:
    youTubeVideoData = json.loads(i)
youTubeVideoData = json.dumps(youTubeVideoData, indent=4)


# Print video info to user
print("Video formats available: ")
for i in range(len(youTubeVideoData["formats"])):
    videoHeight = youTubeVideoData["formats"][i]["height"]
    videoWidth = youTubeVideoData["formats"][i]["width"]
    videoFormat = youTubeVideoData["formats"][i]["format"]
    videoExt = youTubeVideoData["formats"][i]["ext"]
    if "audio only" in videoFormat:
        print("\nAudio Only")
        continue
    formatId = youTubeVideoData["formats"][i]["format_id"]
    formatNote = youTubeVideoData["formats"][i]["format_note"]
    print(str(i + 1) + ". (" + formatId + ") " + formatNote + " " + videoExt)