# Seerr-Route
Automatically change the rootFolder of a requested item depending on whether it is an anime-movie, cartoon, documentary, reality, animated series.

### Instructions
1. Install the requirements
```
pip install -r requirements.txt
```
2. Change the `get_url` and `put_url` to your seerr url
3. Change the rootfolders to match your setup
4. Only uncomment the `request.post` block if you use ntfy


#### TODO:
- Make url, rootfolders, port passable as args or through env
- Add more notification agents (discord, telegram)
