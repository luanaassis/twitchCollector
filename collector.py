import requests
from classes.channel import Channel
from classes.stream import Stream

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

def searchChannels(query):
    endpoint = 'search/channels'
    params = {'query': query}
    response = twitchApiRequestBase(endpoint, params)
    channel_id = response['data'][0]['id']
    return(channel_id)

def getChannelInfo(broadcaster_id):
    endpoint = 'channels'
    params = {'broadcaster_id': broadcaster_id}
    response = twitchApiRequestBase(endpoint, params)
    channel_info = response['data'][0]
    newChannel = Channel(channel_info['broadcaster_id'],channel_info['broadcaster_login'],channel_info['broadcaster_name'],channel_info['broadcaster_language'],
                         channel_info['game_name'],channel_info['game_id'],channel_info['title'],channel_info['tags'], 
                         channel_info['content_classification_labels'], channel_info['is_branded_content'])
    print(newChannel.channel_name,newChannel.stream_tags,newChannel.classification_labels,newChannel.is_branded_content)

def getStream(id):
    endpoint = 'channels'
    params = {'user_id': id}
    response = twitchApiRequestBase(endpoint, params)
    stream_info = response['data'][0]
    newStream = Stream(stream_info['id'],stream_info['user_id'],stream_info['user_login'],stream_info['user_name'],
                    stream_info['language'],stream_info['game_name'], stream_info['game_id'],stream_info['title'],
                    stream_info['tags'],stream_info['type'], stream_info['viewer_count'],stream_info['is_mature'])
    print(newStream.game_name, newStream.stream_title, newStream.is_mature, newStream.stream_tags, newStream.viewer_count)

id = searchChannels('gaules')
getChannelInfo(id)
getStream(id)
