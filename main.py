import json, pprint, os
from googleapiclient.discovery import build

api_key = os.environ.get('YT_API_KEY')
handle  = ''

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part        = 'contentDetails',
    forHandle   = handle
)

response = request.execute()
pprint.pprint(response)