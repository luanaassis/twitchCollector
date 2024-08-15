import pandas as pd
import os
import matplotlib.pyplot as plt

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
df_final = df_mid.drop_duplicates(subset=['Channel Id','Channel Name','Stream/Video Title', 'Game ID'])
df_final = df_final[df_final['Channel Name'].isin(isAdult.keys())]

#Metrics

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

#First graph
consolidated_counts = pd.DataFrame({
    '18+ Games': count_eighteengames_by_influencer,
    'Non-18+ Games': count_NOT_eighteengames_by_influencer
}).fillna(0)
num_channels = len(consolidated_counts)
fig, axes = plt.subplots(num_channels, 1, figsize=(8, 4 * num_channels))
for (channel, counts), ax in zip(consolidated_counts.iterrows(), axes):
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=['red', 'green'])
    ax.set_title(f'Distribuição de Jogos por Classificação Etária para {channel}')

plt.tight_layout()
plt.show()
#Second graph
count_mature_channels_by_influencer.plot(kind='bar', color='red')
plt.title('Número de Canais com Classificação Etária Imprópria por Influenciador')
plt.xlabel('Canal')
plt.ylabel('Número de Canais com Classificação Etária')
plt.show()
#Third graph
count_mature_games_defined_by_influencer.plot(kind='bar', color='red')
plt.title('Canais com Classificação Adulta por Influenciador')
plt.xlabel('Canal')
plt.ylabel('Canais com Classificação Adulta')
plt.show()
#Fourth graph
num_channels = len(counts_top_viewers_by_influencer)
fig, axes = plt.subplots(num_channels, 1, figsize=(8, 4 * num_channels))
if num_channels == 1:
    axes = [axes]
for (channel, counts), ax in zip(counts_top_viewers_by_influencer.iterrows(), axes):
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=['green','red'])
    ax.set_title(f'Distribuição de Indicadores de Classificação dos Videos/Streams mais Visualizadas para {channel}')
plt.tight_layout()
plt.show()
#Fifth graph
if not games_innapropriates_streamedByAdults.empty:
    games_innapropriates_streamedByAdults.plot(kind='bar', color='red')
    plt.title('Quantidade de Jogos Inapropriados Transmitidos por Influencers Adultos')
    plt.xlabel('Canal')
    plt.ylabel('Número de Jogos Inapropriados')
    plt.show()

if not games_innapropriates_streamedByKids.empty:
    games_innapropriates_streamedByKids.plot(kind='bar', color='red')
    plt.title('Quantidade de Jogos Inapropriados Transmitidos por Influencers Crianças')
    plt.xlabel('Canal')
    plt.ylabel('Número de Jogos Inapropriados')
    plt.show()
