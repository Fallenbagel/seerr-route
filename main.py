import os
import requests
from flask import Flask, request
from waitress import serve
from dotenv import load_dotenv

#load the .env file to find any environment variables.
load_dotenv()

#Set variables
seerr_baseurl = os.getenv("seerr_baseurl", None)
seerr_api_key = os.getenv("seerr_api_key", None)
movieFolder_Animemovies = os.getenv("rootFolder_Animemovies", None)
movieFolder_Cartoon = os.getenv("rootFolder_Cartoon", None)
tvFolder_documentary = os.getenv("rootFolder_documentary", None)
tvFolder_Animatedseries = os.getenv("rootFolder_Animatedseries", None)
tvFolder_documentary = os.getenv("rootFolder_documentary", None)
tvFolder_reality = os.getenv("rootFolder_reality", None)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_request():
    request_data = request.get_json()
    process_request(request_data)

    return ('success', 202)

def process_request(request_data):
    request_id = request_data['requestID']
    media_tmdbid = request_data['mediaId']
    media_type = request_data['mediaType']
    image = request_data['image']
    overview = request_data['message']
    print(request_id)
    seasons = None
    if 'extra' in request_data:
        for item in request_data['extra']:
            if item['name'] == 'Requested Seasons':
                seasons = item['value']
                break
    print(seasons)
    get_url = seerr_baseurl + f'/api/v1/{media_type}/{media_tmdbid}?language=en'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': seerr_api_key
    }

    response = requests.get(get_url, headers=headers)
    response_data = response.json()
    print(response_data)

    put_data = None
    if media_type == 'movie':
        if any(g['name'] == 'Animation' for g in response_data['genres']):
            if any(k['name'] == 'anime' for k in response_data['keywords']):
                put_data = {
                    "mediaType": media_type,
                    "rootFolder": movieFolder_Animemovies
                }
            else:
                put_data = {
                    "mediaType": media_type,
                    "rootFolder": movieFolder_Cartoon
                }
        elif any(g['name'] == 'Documentary' for g in response_data['genres']):
            put_data = {
                "mediaType": media_type,
                "rootFolder": tvFolder_documentary
            }
    elif media_type == 'tv':
        seasons = [int(season) for season in seasons.split(',')]
        if any(g['name'] == 'Animation' for g in response_data['genres']) and not any(k['name'] == 'anime' for k in response_data['keywords']):
            put_data = {
                "mediaType": media_type,
                "seasons": seasons,
                "rootFolder": tvFolder_Animatedseries
            }
        elif any(g['name'] == 'Documentary' for g in response_data['genres']):
            put_data = {
                "mediaType": media_type,
                "seasons": seasons,
                "rootFolder": tvFolder_documentary
            }
        elif any(g['name'] == 'Reality' for g in response_data['genres']):
            put_data = {
                "mediaType": media_type,
                "seasons": seasons,
                "rootFolder": tvFolder_reality
            }

    put_url = seerr_baseurl + f'/api/v1/request/{request_id}'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': seerr_api_key,
        'Content-Type': 'application/json'
        }
    if put_data:
        print(put_data)
        requests.put(put_url, headers=headers, json=put_data)
        rootFolder = put_data['rootFolder']
        #title = response_data['title']
        title = response_data.get('title', response_data.get('name', ''))
        print(f"{title}\n{overview}\nRoot Folder: {rootFolder}")
        #requests.post("https://ntfy.sh/requests",
        #data=f"{title}\n{overview}\n\nRoot Folder: {rootFolder}".encode('utf-8'),
        #headers={
        #    "Title": f"Root folder has been changed for the {media_type}",
        #    #"Authorization": "",
        #    "priority": "urgent",
        #    "Attach": image,
        #    "tags": "warning"
        #}
    )
    if response.status_code != 200:
        raise Exception(f'Error updating request status: {response.content}')
    else:
        print("Automatically approve tv show request on Seerr instance, 200")

def handle_request(request):
    request_data = request.get_json()
    process_request(request_data)

    return ('Changed rootfolder', 200)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5001')
