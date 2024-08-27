import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

folder = 'C:\\Users\\luana\\Desktop\\twitchCollector-dev'
files = [f for f in os.listdir(folder) if f.endswith('.xlsx') and f.startswith('twitch_data_tags')]

dataframes = []
pattern = r'\b(?:eighteen|18|CERO_Z)\b'

for file in files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path, engine='openpyxl')
    dataframes.append(df)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)
df_mid = pd.concat(dataframes, ignore_index=True)
df_final = df.drop_duplicates(subset=['Channel Id', 'Stream Title', 'Game ID'], keep='last')

df_final['Source URL'] = df['Source URL'].replace(
    {'https://www.twitch.tv/directory/all/tags/FamilyFriendly': 'FamilyFriendly',
    'https://www.twitch.tv/directory/all/tags/kids': 'Kids',
    'https://www.twitch.tv/directory/all/tags/kid': 'Kid',
    'https://www.twitch.tv/directory/all/tags/kidstreaming': 'KidStreaming',
    'https://www.twitch.tv/directory/all/tags/KidSafe': 'KidSafe',
    'https://www.twitch.tv/directory/all/tags/KidFriendly': 'KidFriendly',
    'https://www.twitch.tv/directory/all/tags/KidGamer': 'KidGamer',
    'https://www.twitch.tv/directory/all/tags/childrens': 'Childrens',
    'https://www.twitch.tv/directory/all/tags/KidsGaming': 'KidsGaming',
    'https://www.twitch.tv/directory/all/tags/childfriendlystream':'ChildFriendlyStream',
    'https://www.twitch.tv/directory/all/tags/kidsandparentsgamers':'KidsAndParentsGamers',
    'https://www.twitch.tv/directory/all/tags/kidshow':'KidShow',
    'https://www.twitch.tv/directory/all/tags/Friendly':'Friendly',
    'https://www.twitch.tv/directory/all/tags/Family':'Family',
    'https://www.twitch.tv/directory/all/tags/Kidsfriendly':'KidsFriendly',
    'https://www.twitch.tv/directory/all/tags/KIDSTREAMER':'KIDSTREAMER',
    'https://www.twitch.tv/directory/all/tags/kidstream':'kidstream'
     })

#Metrics
name_unique_channels = df_final['Channel Name'].unique()
unique_games = df_final.groupby('Source URL')['Game Name'].nunique()

count_mature_classification_by_tag = df_final[df_final['Classification Labels'].notnull()].groupby('Source URL').size()
count_not_mature_classification_by_tag = df_final[df_final['Classification Labels'].isnull()].groupby('Source URL').size()

count_mature_channel_by_tag = df_final[df_final['Is Mature'] == 1].groupby('Source URL').size()
count_not_mature_channel_by_tag = df_final[df_final['Is Mature'] == 0].groupby('Source URL').size()

count_eighteen_by_tag = df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False)].groupby('Source URL').size()
count_not_eighteen_by_tag = df_final[~df_final['Age Rating'].str.contains(pattern, case=False, na=False)].groupby('Source URL').size()

top_viewers_df = (
    df_final.groupby('Source URL')
    .apply(lambda x: x.nlargest(10, 'Viewer Count'))
    .reset_index(drop=True))
top_viewers_df['Age Ratings Indicator'] = top_viewers_df['Age Rating'].str.contains(pattern).astype(int)
counts_top_viewers = top_viewers_df.groupby('Source URL')['Age Ratings Indicator'].value_counts().unstack(fill_value=0)

most_played_games_by_tag = df_final.groupby('Source URL')['Game Name'].value_counts()
most_played_games_by_tag = most_played_games_by_tag.reset_index(name='Count')
result_most_played_games_by_tag = pd.merge(most_played_games_by_tag, df_final[['Source URL', 'Game Name', 'Age Rating']], on=['Source URL', 'Game Name'], how='left')
result_most_played_games_by_tag = result_most_played_games_by_tag.drop_duplicates(subset=['Source URL', 'Game Name','Age Rating'])
result_most_played_games_by_tag['Age Ratings Indicator'] = result_most_played_games_by_tag['Age Rating'].str.contains(pattern).astype(int)
counts_popular_games = top_viewers_df.groupby('Source URL')['Age Ratings Indicator'].value_counts()

top_10_most_played_games_by_tag = result_most_played_games_by_tag.groupby('Source URL').apply(lambda x: x.nlargest(10, 'Count'))
top_10_most_played_games_by_tag = top_10_most_played_games_by_tag.reset_index(drop=True)

mature_channel = df_final[df_final['Is Mature'] == 1]
mature_channel_tag = mature_channel[['Stream Tags', 'Source URL']]

games_eighteen_by_tag = df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False)][['Source URL', 'Game Name', 'IGDB ID']].drop_duplicates()

#print(name_unique_channels) #Nome dos canais buscados
#print(games_eighteen_by_tag) #Diferentes jogos +18
#print(top_viewers_df) #Resultados de Q4 para justificar
#print(top_10_most_played_games_by_tag) #Resultados de Q3 para justificar
#print(mature_channel_tag) #Analisar tags com conteúdo promocional

#First graph
comparison_df = pd.DataFrame({
    'Canais com classificação adulta': count_mature_classification_by_tag,
    'Canais sem classificação adulta': count_not_mature_classification_by_tag
})
comparison_df = comparison_df.fillna(0)
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#ff0000', '#0000ff'] 
comparison_df.plot(kind='bar', ax=ax, color=colors)
ax.set_xlabel('Tag')
ax.set_ylabel('Quantidade')
ax.set_title('Comparação entre Contagem de Canais com Classificação Adulta e Canais Sem Classificação por TAG')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Second graph
comparison_df = pd.DataFrame({
    'Canais adultos': count_mature_channel_by_tag,
    'Canais não adultos': count_not_mature_channel_by_tag
})
comparison_df = comparison_df.fillna(0)
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#ff0000', '#0000ff'] 
comparison_df.plot(kind='bar', ax=ax, color=colors)
ax.set_xlabel('Tag')
ax.set_ylabel('Quantidade')
ax.set_title('Comparação entre Contagem de com e sem Conteúdo Promocional por TAG')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Third graph
comparison_df = pd.DataFrame({
    'Jogos adultos': count_eighteen_by_tag,
    'Jogos não adultos': count_not_eighteen_by_tag
})
comparison_df = comparison_df.fillna(0)
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#ff0000', '#0000ff'] 
comparison_df.plot(kind='bar', ax=ax, color=colors)
ax.set_xlabel('Tag')
ax.set_ylabel('Quantidade')
ax.set_title('Comparação entre Contagem de Jogos Adultos e Jogos Não Adultos por TAG')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Fouth graph
colors = ['#0000ff','#ff0000']
counts_top_viewers.plot(kind='bar', stacked=True, color=colors)
plt.title('Classificação dos jogos exibidos nas streams mais visualizadas por Tag')
plt.xlabel('Tag')
plt.ylabel('Quantidade')
plt.show()

#Fifth graph
colors = ['#0000ff','#ff0000']
counts_popular_games.plot(kind='bar', stacked=True, color=colors)
plt.title('Classificação dos jogos mais exibidos nas streams por Tag')
plt.xlabel('Tag')
plt.ylabel('Quantidade')
plt.show()
