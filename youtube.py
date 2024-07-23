# Import modules
import os
from tqdm import tqdm
import pygsheets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Access client key
CLIENT_SECRETS_FILE = "client_secret_key.json"  # Name of the JSON file

# Access Google Sheets
gc = pygsheets.authorize(outh_file='credentials.json')
sheet = gc.open_by_key('1iT680JWO-5zAOweypNvCp51K3A6lp9BTCwfZUWh6YIU')

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
service = get_authenticated_service()

# =============================================================================
# Search Query Initialisation
# =============================================================================

query = input('Please type the keyword you want to search for: ')
videos_to_analyse = int(
    input('Please type how many videos you want to analyse: '))
comments_search_results = int(
    input('Please type how many replies per video you want to analyse: '))
pages_to_pull = (videos_to_analyse // 50) + 1

video_id = []
channel = []
video_title = []
video_desc = []

count = 0

if count == 0:
    count += 1
    query_results = service.search().list(
        part='snippet',
        q=query,
        order='relevance',  # You can also change it to viewcount
        maxResults=50,
        type='video',
        relevanceLanguage='en',
        safeSearch='moderate',
    ).execute()
    page_token_id = query_results['nextPageToken']

    for item in tqdm(query_results['items']):
        video_id.append(item['id']['videoId'])
        channel.append(item['snippet']['channelTitle'])
        video_title.append(item['snippet']['title'])
        video_desc.append(item['snippet']['description'])

for num in range(1, pages_to_pull):

    query_results = service.search().list(
        part='snippet',
        q=query,
        order='relevance',  # You can also change it to viewcount
        maxResults=50,
        pageToken=page_token_id,
        type='video',
        relevanceLanguage='en',
        safeSearch='moderate',
    ).execute()

    page_token_id = query_results['nextPageToken']

    for item in tqdm(query_results['items']):
        video_id.append(item['id']['videoId'])
        channel.append(item['snippet']['channelTitle'])
        video_title.append(item['snippet']['title'])
        video_desc.append(item['snippet']['description'])

# =============================================================================
# Get Comments of Top Videos
# =============================================================================
video_id_pop = []
channel_pop = []
video_title_pop = []
video_desc_pop = []
comments_pop = []
comment_id_pop = []
reply_count_pop = []
like_count_pop = []

for i, video in enumerate(tqdm(video_id)):
    try:
        response = service.commentThreads().list(
            part='snippet',
            videoId=video,
            # Takes the users input for how many comments to analyse...
            maxResults=comments_search_results,
            order='relevance',  # ... ranked on relevance
            textFormat='plainText',
        ).execute()
    except:
        continue

    comments_temp = []
    comment_id_temp = []
    reply_count_temp = []
    like_count_temp = []

    for item in response['items']:
        comments_temp.append(
            item['snippet']['topLevelComment']['snippet']['textDisplay'])
        comment_id_temp.append(item['snippet']['topLevelComment']['id'])
        reply_count_temp.append(item['snippet']['totalReplyCount'])
        like_count_temp.append(
            item['snippet']['topLevelComment']['snippet']['likeCount'])

    comments_pop.extend(comments_temp)
    comment_id_pop.extend(comment_id_temp)
    reply_count_pop.extend(reply_count_temp)
    like_count_pop.extend(like_count_temp)

    video_id_pop.extend([video_id[i]] * len(comments_temp))
    channel_pop.extend([channel[i]] * len(comments_temp))
    video_title_pop.extend([video_title[i]] * len(comments_temp))
    video_desc_pop.extend([video_desc[i]] * len(comments_temp))

query_pop = [query] * len(video_id_pop)

import pandas as pd


output_dict = {
    'Query': query_pop,
    'Channel': channel_pop,
    'Video Title': video_title_pop,
    'Comment': comments_pop,
    'Likes': like_count_pop,
    'Replies': reply_count_pop,
    'Video Description': video_desc_pop,
    'Video ID': video_id_pop,
    'Comment ID': comment_id_pop,


}
first_worksheet = sheet.worksheet_by_title('Sheet1')
first_worksheet.clear(start='A1')
output_df = pd.DataFrame(output_dict, columns=output_dict.keys())
first_worksheet.set_dataframe(output_df, start='A1', nan='')

print("Success!\nPlease check your Google sheets now.")
