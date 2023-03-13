import requests
from flask import Flask, request
from waitress import serve

app = Flask(__name__)


#### Configure here your settings

overseerr_baseurl = "http://xxx.xx.x.xx:5055"
overseerr_api_key = "API token"

#### Configuration for Sonarr TV-Show
tvshow_sonarrserver_name = "Servername"
tvshow_sonarrserver_Id = 0
tvshow_rootfolder = "/data/media/tv"

#### Configuration for Sonarr Anime
anime_sonarrserver_name = "Servername"
anime_sonarrserver_Id = 1
anime_rootfolder = "/data/media/anime"





@app.route('/webhook', methods=['POST'])
def handle_request():
    request_data = request.get_json()
    process_request(request_data)

    return ('success', 202)

def process_request(request_data):
    request_username = request_data['requestUserName']
    request_id = request_data['requestID']
    media_tmdbid = request_data['mediaId']
    media_type = request_data['mediaType']
    image = request_data['image']
    overview = request_data['message']
    print(f"Overseerr webhook received for a new tv-show request by {request_username}")
    #print(request_id)
    seasons = None
    if 'extra' in request_data:
        for item in request_data['extra']:
            if item['name'] == 'Requested Seasons':
                seasons = item['value']
                break
    #print(seasons)
    get_url = overseerr_baseurl + f'/api/v1/{media_type}/{media_tmdbid}?language=en'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': overseerr_api_key
    }

    response = requests.get(get_url, headers=headers)
    response_data = response.json()
   # print(response_data)
    print(f"Reading data with requestID {request_id} to determine how to process the request")
    put_data = None
    
    if media_type == 'movie':
        if any(g['name'] == 'Animation' for g in response_data['genres']):
            if any(k['name'] == 'anime' for k in response_data['keywords']):
                put_data = {
                    "mediaType": media_type,
                    "rootFolder": "/mnt/media/Animemovies"
                    "serverId": anime_sonarrserver_Id
                }
            else:
                put_data = {
                    "mediaType": media_type,
                    "rootFolder": "/mnt/media/Cartoon"
                }
        elif any(g['name'] == 'Documentary' for g in response_data['genres']):
            put_data = {
                "mediaType": media_type,
                "rootFolder": "/mnt/media/documentary"
            }
    
    elif media_type == 'tv':
        seasons = [int(season) for season in seasons.split(',')]
        if any(g['name'] == 'Animation' for g in response_data['genres']) and any(k['name'] == 'anime' for k in response_data['keywords']):
            put_data = {
                "mediaType": media_type,
                "seasons": seasons,
                "rootFolder": anime_rootfolder,
                "serverId": anime_sonarrserver_Id
            }
            TargetSonarrServer = anime_sonarrserver_name
        else:
            put_data = {
                    "mediaType": media_type,
                    "seasons": seasons,
                    "rootFolder": tvshow_rootfolder,
                    "serverId": tvshow_sonarrserver_Id
				}
            TargetSonarrServer = tvshow_sonarrserver_name

    put_url = overseerr_baseurl + f'/api/v1/request/{request_id}'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': overseerr_api_key,
        'Content-Type': 'application/json'
        }
    if put_data:
        requests.put(put_url, headers=headers, json=put_data)
    if response.status_code != 200:
      raise Exception(f'Error applying backend server overwrite in Overseerr: {response.content}')
    else:
      print(f"Successfully modified target backend tv processing server to {TargetSonarrServer} in Overseerr")
    post_url = overseerr_baseurl + f'/api/v1/request/{request_id}/approve'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': overseerr_api_key,
        'Content-Type': 'application/json'
        }
    requests.post(post_url, headers=headers)
    if response.status_code != 200:
      raise Exception(f'Error updating request status: {response.content}')
    else:
      print("Automatically approve tv show request on Overseerr instance")
      
def handle_request(request):
    request_data = request.get_json()
    process_request(request_data)

    return ('Changed rootfolder and server', 200)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5001')
