import pprint, os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

client_secret   = os.environ.get('YT_CLIENT_SECRET_PATH')
credentials = None

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists('token.pickle'):
    print('Loading credentials from file..')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

# if there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret,
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/youtube.force-ssl'
            ]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)
request = youtube.videos().list(
    part        = ['snippet', 'contentDetails', 'statistics'],
    myRating    = 'like',
    maxResults   = 50
)

response = request.execute()

#pprint.pprint(response['items'])

sb19_channelId  = 'UCm4v7afBTnJKRm4SlfHJzyg'
darla_channelId = 'UCP50end1PCEhV4sWEygmQaQ'

#Un-like the videos from the listed channels
for liked_video in response['items']:
    if liked_video['snippet']['channelId'] == sb19_channelId or liked_video['snippet']['channelId'] == darla_channelId:
        print(f'Unliking: https://www.youtube.com/watch?v={liked_video['id']}')

        unlike_request = youtube.videos().rate(
            id = liked_video['id'],
            rating = 'none'
        )

        unlike_response = unlike_request.execute()
        print(unlike_response)




