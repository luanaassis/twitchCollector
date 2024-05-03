import requests
import datetime
import schedule
import time
from classes.channel import Channel
from classes.stream import Stream
from classes.game import Game
from classes.category import Category
from classes.user import User

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
    login = response['data'][0]['broadcaster_login']
    return(channel_id,login)

def getChannelInfo(broadcaster_id):
    endpoint = 'channels'
    params = {'broadcaster_id': broadcaster_id}
    response = twitchApiRequestBase(endpoint, params)
    channel_info = response['data'][0]
    newChannel = Channel(channel_info['broadcaster_id'],channel_info['broadcaster_login'],channel_info['broadcaster_name'],channel_info['broadcaster_language'],
                         channel_info['game_name'],channel_info['game_id'],channel_info['title'],channel_info['tags'], 
                         channel_info['content_classification_labels'], channel_info['is_branded_content'])
    print(newChannel.channel_name,newChannel.stream_tags,newChannel.classification_labels,newChannel.is_branded_content)

def getStreams(id):
    endpoint = 'streams'
    params = {'user_id': id}
    response = twitchApiRequestBase(endpoint, params)
    stream_info_qty = len(response['data'])
    for i in range(stream_info_qty):
        stream_info = response['data'][i]
        newStream = Stream(stream_info['id'],stream_info['user_id'],stream_info['user_login'],stream_info['user_name'],
                    stream_info['language'],stream_info['game_name'], stream_info['game_id'],stream_info['title'],
                    stream_info['tags'],stream_info['type'], stream_info['viewer_count'],stream_info['is_mature'])
        print(newStream.game_name, newStream.stream_title, newStream.is_mature, newStream.stream_tags, newStream.viewer_count)

def getTopGames():
    endpoint = 'games/top'
    response = twitchApiRequestBase(endpoint, None)
    game_info_qty = len(response['data'])
    for i in range(game_info_qty):
        game_info = response['data'][i]
        newGame = Game(game_info['id'],game_info['name'],game_info['igdb_id'],True,datetime.datetime.now())
        print(newGame.name,newGame.isTopGame,newGame.dateTop)

def getGame(id):
    endpoint = 'games'
    params = {'id': id}
    response = twitchApiRequestBase(endpoint, params)
    game_info= response['data'][0]
    newGame = Game(game_info['id'],game_info['name'],game_info['igdb_id'],False,None)
    print(newGame.name,newGame.isTopGame,newGame.dateTop)

def getCategories(query):
    endpoint = 'search/categories'
    params = {'query': query}
    response = twitchApiRequestBase(endpoint, params)
    category_info_qty = len(response['data'])
    for i in range(category_info_qty):
        category_info = response['data'][i]
        newCategory = Category(category_info['id'],category_info['name'])
        print(newCategory.id, newCategory.name)

def getUser(id, login):
    endpoint = 'users'
    params = {'id': id, 'login': login}
    response = twitchApiRequestBase(endpoint, params)
    user_info_qty = len(response['data'])
    for i in range(user_info_qty):
        user_info = response['data'][i]
        newUser = User(user_info['id'],user_info['login'],user_info['display_name'],user_info['type'],
                       user_info['broadcaster_type'], user_info['description'],user_info['created_at'])
        print(newUser.user_name,newUser.broadcast_contract_type,newUser.channel_description,newUser.created_at)

schedule.every().hour.do(getTopGames)
while True:
    schedule.run_pending()
    time.sleep(3600)