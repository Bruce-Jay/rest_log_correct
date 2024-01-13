# change `data` variable into your own data (e.g, url, params), and run the following code to get the execution value of API request
import requests
import yaml
from langchain.requests import Requests
import os
import json
import spotipy

################# Http headers ################
config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
os.environ['SPOTIPY_CLIENT_ID'] = config['spotipy_client_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config['spotipy_client_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config['spotipy_redirect_uri']
with open("spotify_oas.json") as f:
    raw_api_spec = json.load(f)
scopes = list(raw_api_spec['components']['securitySchemes']['oauth_2_0']['flows']['authorizationCode']['scopes'].keys())
access_token = spotipy.util.prompt_for_user_token(scope=','.join(scopes))
headers = {
    'Authorization': f'Bearer {access_token}'
}

requests_wrapper = Requests(headers=headers)
spotify_user_id = config['spotify_user_id']
################# Http headers ################


################# request_data ###############
# change the `data` with your own data to request http server
method='PUT' # choice: GET, POST, PUT, DELETE
data={
    "url": "https://api.spotify.com/v1/me/player/repeat",
    "params": {
        "state": "track"
    },
    "description": "The API response is empty."
}

################# request_data ###############


################# request from http serve and print the execution result ###############
if method == "GET":
    if 'params' in data:
        params = data.get("params", [])
        response = requests_wrapper.get(data.get("url"), params=params)
    else:
        response = requests_wrapper.get(data.get("url"))
elif method == "POST":
    params = data.get("params")
    request_body = data.get("data")
    response = requests_wrapper.post(data["url"], params=params, data=request_body)
elif method == "PUT":
    params = data.get("params")
    request_body = data.get("data")
    response = requests_wrapper.put(data["url"], params=params, data=request_body)
elif method == "DELETE":
    params = data.get("params")
    request_body = data.get("data")
    response = requests_wrapper.delete(data["url"], params=params, json=request_body)
else:
    raise NotImplementedError
response_text = response.text

# 把内容保存到文件中
# print(response_text)
with open('output.json', 'w', encoding='utf-8') as f:
    f.write(response_text)
################# request from http serve and print the execution result ###############

response_json = json.loads(response_text)

