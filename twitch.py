import config
import requests
import json
import csv

#this was mostly messing around with the twitch api calls.

base_url ='https://api.twitch.tv/helix/'
client_id = config.api_key
headers = {'Client-ID': client_id}
indent = 2

def get_response(query):
    url = base_url + query
    response = requests.get(url, headers=headers)
    return response

def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json, indent=indent)
    print(print_response)

def get_top_league_clips():
    return 'clips?game_id=21779&first=5'

#Function that runs the API call and creates the CSV file to be read in base.py
def do_it():
    query = get_top_league_clips()
    response = get_response(query)
    clipurls = response.json()
    listofclips = clipurls['data']


    clip_data = open('clipdata.csv', 'w', newline='')
    csvwriter = csv.writer(clip_data)

    for link in listofclips:
        try:
            csvwriter.writerow([link['url'], link['broadcaster_name'], link['title']])
        except UnicodeEncodeError:
            pass

do_it()