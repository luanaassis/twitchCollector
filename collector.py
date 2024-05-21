import requests
import datetime
import time
from classes.channel import Channel
from classes.stream import Stream
from classes.game import Game
from classes.category import Category
from classes.user import User
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

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

def searchChannels(query, live_only):
    endpoint = 'search/channels'
    params = {'query': query, 'live_only': live_only}
    response = twitchApiRequestBase(endpoint, params)
    channel_id = response['data'][0]['id']
    login = response['data'][0]['broadcaster_login']
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
    return newChannel


def getStreams(id, type):
    endpoint = 'streams'
    params = {'user_id': id, 'type': type}
    response = twitchApiRequestBase(endpoint, params)
    stream_info_qty = len(response['data'])
    for i in range(stream_info_qty):
        stream_info = response['data'][i]
        newStream = Stream(stream_info['id'],stream_info['user_id'],stream_info['user_login'],stream_info['user_name'],
                    stream_info['language'],stream_info['game_name'], stream_info['game_id'],stream_info['title'],
                    stream_info['tags'],stream_info['type'], stream_info['viewer_count'],stream_info['is_mature'])
        print(newStream.game_name, newStream.stream_title, newStream.is_mature, newStream.stream_tags, newStream.viewer_count)
        return newStream

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

def searchKidsTag():
    chrome_driver_path = r'C:\Users\luana\Desktop\chromedriver-win64\chromedriver.exe'

    service = Service(chrome_driver_path)
    service.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = 'https://www.twitch.tv/directory/all/tags/kids'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-focusable="true"][data-test-selector="TitleAndChannel"][data-a-target="preview-card-channel-link"]')))
        channel_names = []
        
        for element in elements:
            channel_URL = (element.get_attribute('href'))
            channel_name = channel_URL.replace('https://www.twitch.tv/', '')
            print("Parte relevante da URL:", channel_name)
            channel_names.append(channel_name)

    finally:
        driver.quit()
        return channel_names

def main():
    while True:
        channels = searchKidsTag()
        wb = Workbook()
        ws = wb.active
        ws.append(['SearchTime','Channel Id','Channel Name','Language','Classification Labels' ,'Stream Title','Game ID','Game Name', 'Is Mature', 'Stream Tags', 'Viewer Count'])
        for channel in channels:
           id = searchChannels(channel,True)
           channel_info = getChannelInfo(id)
           stream_info = getStreams(id, 'live')
           ws.append([datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),channel_info.id,channel_info.channel_name,channel_info.language, channel_info.classification_labels,stream_info.stream_title,stream_info.game_id,stream_info.game_name,stream_info.is_mature, ', '.join(channel_info.stream_tags), stream_info.viewer_count])
        filename = f"twitch_data_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        wb.save(filename)
        time.sleep(3600)

if __name__ == "__main__":
    main()
