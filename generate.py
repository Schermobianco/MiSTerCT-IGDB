import requests
import os

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)

#data output
keys = r.json()

print(keys)

headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}

print(headers)