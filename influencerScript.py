import pandas as pd
import os

folder = 'C:\\Users\\luana\\Desktop\\twitchCollector-dev'
files = [f for f in os.listdir(folder) if f.endswith('.xlsx') and f.startswith('twitch_data_influencers')]

isAdult = {
    "felipeneto": 1,
    "rezendeevil": 1,
    "paitambemjoga": 1,
    "paitambemjogalive": 1,
    "camilalouresoficial": 1,
    "enaldinho": 1,
    "kidplayerr": 0,
    "loud_thurzin": 0,
    "jeanmago": 1,
    "rowdyroganfam": 0,
    "zenonlives": 0,
    "evantube": 1,
    "piperrockelle16": 1,
    "levcameron": 1,
    "queenkhamyra": 1,
    "charlidamelioop": 1,
    "mongraal": 1,
    "captainsparklez": 1,
    "ldshadowlady": 1,
    "grianmc": 1,
    "itsfunneh": 1,
    "chuggaaconroy": 1,
    "blitz": 1
}

patternInapropriate = r'\b(?:eighteen|18|CERO_Z)\b'

dataframes = []

for file in files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path, engine='openpyxl')
    dataframes.append(df)

df_final = pd.concat(dataframes, ignore_index=True)

top_viewers = df.nlargest(10, 'Viewer Count') # mais vistos
count_inapropriateGame = df_final['Age Rating'].str.contains(patternInapropriate, case=False, na=False).sum() # quantidade de conteúdos 18+
count_mature_games = df_final['Is Mature'].sum() # quantidade de jogos classificados com 18+
count_mature_channels = df_final['Classification Labels'].notnull().sum() # quantidade de canais classificados com 18+
inappropriate_top_viewers = top_viewers[top_viewers['Age Rating'].str.contains(patternInapropriate, case=False, na=False)] #mais vistos classificados com 18+
count_inappropriate_top_viewers = inappropriate_top_viewers.shape[0] # quantos dos mais vistos são classificados com 18+
df_final['isAdult'] = df_final['Channel Name'].map(isAdult) #adicionando informação se é adulto ou não
inappropriate_contents = df_final[df_final['Age Rating'].str.contains(patternInapropriate, case=False, na=False)] #conteúdos +18
count_adult_inappropriate = inappropriate_contents[inappropriate_contents['isAdult'] == 1].shape[0] #conteúdos +18 de canais adultos
count_non_adult_inappropriate = inappropriate_contents[inappropriate_contents['isAdult'] == 0].shape[0] #conteúdos +18 de canais -18
