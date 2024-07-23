# YouTube Comment Analyzer

This Python script allows you to search for YouTube videos based on a keyword, collect comments from these videos, and save the results to a Google Sheet.

## Features

- Search YouTube videos by keyword
- Collect top comments from the most relevant videos
- Save results to a Google Sheet, including:
  - Search query
  - Channel name
  - Video title
  - Comment text
  - Number of likes on comments
  - Number of replies to comments
  - Video description
  - Video ID
  - Comment ID

## Prerequisites

Before running this script, you need to have:

1. Python 3.x installed
2. A Google account
3. A Google Cloud project with the YouTube Data API v3 enabled
4. OAuth 2.0 credentials for YouTube Data API
5. Google Sheets API credentials

## Required Python Libraries

- os
- tqdm
- pygsheets
- google-api-python-client
- google-auth-oauthlib
- pandas

## Setup

1. Place your OAuth 2.0 credentials file (renamed to `client_secret_key.json`) in the same directory as the script.
2. Place your Google Sheets API credentials file (named `credentials.json`) in the same directory as the script.
3. Update the `sheet = gc.open_by_key('')` line with your Google Sheet's ID.

## Usage

1. Run the script

2. When prompted, enter:
- The keyword you want to search for
- The number of videos you want to analyze
- The number of comments per video you want to analyze

3. The script will then:
- Search for videos based on your keyword
- Collect comments from these videos
- Save the results to your specified Google Sheet

## Configuration

- The script is set to search for English language content (`relevanceLanguage='en'`).
- Safe search is set to moderate (`safeSearch='moderate'`).
- Comments are sorted by relevance (`order='relevance'`).

You can modify these settings in the code if needed.

## Note

This script uses the YouTube Data API, which has quota limits. Be mindful of these limits when using the script, especially when requesting a large number of videos or comments.

