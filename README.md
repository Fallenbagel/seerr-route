# Seerr-Route
Automatically change the rootFolder of a requested item depending on whether it is an anime-movie, cartoon, documentary, reality, animated series.

### Instructions
1. Install the requirements
```
pip install -r requirements.txt
```
2. Change the `get_url` and `put_url` to your seerr url
3. Also add in your api-keys into the headers of both under `'X-Api-Key':`
3. Change the rootfolders to match your setup
4. Only uncomment the `request.post` block if you use ntfy
5. Run with `python main.py` or `python main.py &`(detached)
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

#### TODO:
- Make url, rootfolders, port passable as args or through env
- Add more notification agents (discord, telegram)
- Add in a python binary with all dependencies packaged into it
