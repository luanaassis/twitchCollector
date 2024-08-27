import pandas as pd
import os
import datetime

folder = 'C:\\Users\\luana\\Desktop\\twitchCollector-dev'
files = [f for f in os.listdir(folder) if f.endswith('.xlsx') and f.startswith('twitch_data_influencers')]

isAdult = {
    "felipeneto_oficial": 1,
    "rezendeevil33": 1,
    "paitambemjoga": 1,
    "PaiTambemJogaLive": 1,
    "camilalouresoficial": 1,
    "enaldinho_fan_clube": 1,
    "KidPlayerr": 0,
    "loud_thurzin4": 0,
    "jeanmago1020": 1,
    "rowdyroganfan12346": 0,
    "ZenonLives": 0,
    "evantube_inactive_200228": 1,
    "piperrockelle3134433": 1,
    "leocameron1234": 1,
    "queenkayra": 1,
    "charlidameliooo": 1,
    "mongraal_watchparty": 1,
    "CaptainSparklez": 1,
    "ldshadowlady10221872011": 1,
    "grainmcd": 1,
    "itsfunnehlolhrh": 1,
    "Chuggaaconroybot": 1,
    "Blitzcrank": 1
}

patternInapropriate = r'\b(?:eighteen|18|CERO_Z)\b'

dataframes = []

for file in files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path, engine='openpyxl')
    dataframes.append(df)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)
df_mid = pd.concat(dataframes, ignore_index=True)
df_final = df.drop_duplicates(subset=['Channel Id', 'Stream/Video Title', 'Game ID'], keep='last')

#Metrics
unique_channels = df_final['Channel Id'].nunique()
unique_games = df_final['Game Name'].nunique()
unique_videos_lives = df_final['Stream/Video Title'].nunique()

tags_used_by_influencers = df_final.groupby('Channel Name')['Stream Tags'].apply(lambda x: ', '.join(x.dropna().unique())).reset_index()

count_eighteengames_by_influencer = df_final[df_final['Age Rating'].str.contains(patternInapropriate, case=False, na=False)].groupby('Channel Name').size()
count_NOT_eighteengames_by_influencer = df_final[~df_final['Age Rating'].str.contains(patternInapropriate, case=False, na=False)].groupby('Channel Name').size()

count_mature_channels_by_influencer = df_final[df_final['Classification Labels'].notnull()].groupby('Channel Name').size()

count_mature_games_defined_by_influencer = df_final.groupby('Channel Name')['Is Mature'].sum()

top_viewers_by_influencer = df_final.groupby('Channel Name').apply(lambda x: x.nlargest(20, 'Viewer Count')).reset_index(drop=True)
colunas_desejadas = ['Game Name', 'Viewer Count', 'Age Rating','Channel Name', 'Stream/Video Title']
top_viewers_by_influencer = top_viewers_by_influencer[colunas_desejadas]
top_viewers_by_influencer['Age Rating Flag'] = top_viewers_by_influencer['Age Rating'].str.contains(patternInapropriate).astype(float)
counts_top_viewers_by_influencer = top_viewers_by_influencer.groupby('Channel Name')['Age Rating Flag'].value_counts().unstack(fill_value=0)

isAdult = pd.DataFrame(list(isAdult.items()), columns=['Channel Name', 'Is Adult'])
isAdultMerged = pd.merge(df_final, isAdult, on='Channel Name')
isAdultFiltered = isAdultMerged[isAdultMerged['Is Adult'] == 1]
isKidFiltered = isAdultMerged[isAdultMerged['Is Adult'] == 0]

games_innapropriates_streamedByAdults = isAdultFiltered[isAdultFiltered['Age Rating'].str.contains(patternInapropriate, case=False, na=False)].groupby('Channel Name').size()
games_innapropriates_streamedByKids = isKidFiltered[isKidFiltered['Age Rating'].str.contains(patternInapropriate, case=False, na=False)].groupby('Channel Name').size()

#print(tags_used_by_influencers) #Tags utilizadas pelos influencers

output_file = f'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\output_influencers_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Existe diferença na classificação de jogos exibidos por influenciadores infantis com - de 18 anos com influenciadores infantis que possuem + de 18 anos?\n' )
    f.write('Influenciadores infantis com - de 18 anos:\n')
    for influencer, count in games_innapropriates_streamedByKids.items():
        proportion = (count / unique_games_streamedByKids) * 100
        f.write(f"Influencer: {influencer}, Count: {count}, Total:{unique_games_streamedByKids}, Proportion: {proportion:.2f}%\n")
    f.write('Influenciadores infantis com + de 18 anos:\n')
    for influencer, count in games_innapropriates_streamedByAdults.items():
        proportion = (count / unique_games_streamedByAdults) * 100
        f.write(f"Influencer: {influencer}, Count: {count}, Total:{unique_games_streamedByAdults}, Proportion: {proportion:.2f}%\n")
    f.write('Os jogos de influenciadores para o publico infantil sao apropriados para este publico?\n' )
    for influencer, count in count_eighteen_by_influencer.items():
        proportion = (count / unique_games) * 100
        f.write(f"Influencer: {influencer}, Count: {count}, Total:{unique_games}, Proportion: {proportion:.2f}%\n")
    f.write('Os conteúdos mais visualizados dentre estes influenciadores são de conteúdos apropriados ao público infantil?\n' )
    f.write(f"\n{top_viewers_by_influencer}\n")
    f.write('A classificação do canal e dos jogos foram devidamente indicados no canal destes influenciadores?\n' )
    f.write('Canais marcados como adultos:\n')
    for influencer, count in count_mature_channels_by_influencer.items():
        proportion = (count / unique_channels) * 100
        f.write(f"Influencer: {influencer}, Count: {count}, Total:{unique_channels}, Proportion: {proportion:.2f}%\n")
    f.write('Canais com jogos marcados como adultos: \n')
    for influencer, count in filtered_results_count_mature_games_defined_by_influencer.items():
        proportion = (count / unique_games) * 100
        f.write(f"Influencer: {influencer}, Count: {count}, Total:{unique_games}, Proportion: {proportion:.2f}%\n")
    
