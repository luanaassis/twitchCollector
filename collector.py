import requests

client_id = ''
client_secret = ''

def get_access_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data.get('access_token')

def twitchApiRequestBase(endpoint, params=None):
    base_url = 'https://api.twitch.tv/helix/'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {get_access_token(client_id, client_secret)}'
    }
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    return response.json()

def searchGame():
    endpoint = 'games'
    params = {'id': 33214}
    response = twitchApiRequestBase(endpoint, params)
    return response['data']

game = searchGame()
game_info = game[0]
game_name = game_info['name']
print("Name:", game_name)