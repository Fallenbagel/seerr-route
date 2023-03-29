# Seerr-Route
Automatically change the rootFolder of a requested item depending on whether it is an anime-movie, cartoon, documentary, reality, animated series.

### Instructions
#### Native
1. Install the requirements
```
pip install -r requirements.txt
```
2. Configure the .env file to your needs
4. Only uncomment the `request.post` block if you use ntfy
5. Run with `python main.py` or `nohup python main.py &`(detached)
6. In Seerr, turn on `webhook notification agent` and enable `request pending approval` notification type
7. Add the url for the webhook, for example, `192.168.1.5:5001/webhook`
8. Add the following template and save
```
{
  "requestID": "{{request_id}}",
  "mediaId": "{{media_tmdbid}}",
  "mediaType": "{{media_type}}",
  "{{extra}}": [],
  "image": "{{image}}",
  "message": "{{message}}"
}
```

#### Docker (Manual)
1. Clone this repo
2. Navigate to the rootfolder of this repo
3. Run
```
docker build -t seerr-route .
```
4. Configure the .env file
5. Run the docker container with the env file passed in
```
docker run --env-file ./.env seerr-route
```

#### TODO:
~~- Make url, rootfolders, port passable as args or through env~~
- Add more notification agents (discord, telegram)
- Make notifications selectable especially for docker
- Push image to dockerhub/ghcr.io
- Create a docker-compose
- Configure CI workshops to build Docker inage
- Add in a python binary with all dependencies packaged into it
