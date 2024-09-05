import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

folder = 'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\apresentacao'
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
df_final = df_mid.drop_duplicates(subset=['Channel Id', 'Stream Title', 'Game ID'], keep='last')

df_final['Source URL'] = df_final['Source URL'].replace(
    {'https://www.twitch.tv/directory/all/tags/FamilyFriendly': 'FamilyFriendly',
    'https://www.twitch.tv/directory/all/tags/kids': 'Kids',
    'https://www.twitch.tv/directory/all/tags/kid': 'Kid',
    'https://www.twitch.tv/directory/all/tags/Kidstreaming': 'KidStreaming',
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

df_final['SearchTime'] = pd.to_datetime(df_final['SearchTime'])
df_final['Hour'] = df_final['SearchTime'].dt.hour
df_final['DayType'] = df_final['SearchTime'].dt.weekday.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
df_final['DayWeek'] = df_final['SearchTime'].dt.day_name()

#Metrics
tags_from_family_friendly = df_final.loc[df_final['Source URL'] == 'FamilyFriendly', 'Stream Tags']
todas_as_tags = tags_from_family_friendly.str.split(', ').explode()
frequencia_tags = todas_as_tags.value_counts()

grouped_by_hour = df_final[['Hour', 'Source URL']]
grouped_by_hour = grouped_by_hour.groupby(['Hour', 'Source URL']).size().reset_index(name='Quantity')

grouped_by_day = df_final[['DayType', 'Source URL']]
grouped_by_day = grouped_by_day.groupby(['DayType', 'Source URL']).size().reset_index(name='Quantity')

grouped_by_day_of_week = df_final[['DayWeek', 'Source URL']]
grouped_by_day_of_week = grouped_by_day_of_week.groupby(['DayWeek', 'Source URL']).size().reset_index(name='Quantity')

name_unique_channels = df_final.groupby('Source URL')['Channel Name'].unique()
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
average_audience = df_final.groupby('Source URL')['Viewer Count'].mean().reset_index()

#print(name_unique_channels) #Nome dos canais buscados
#print(games_eighteen_by_tag) #Diferentes jogos +18
#print(top_viewers_df) #Resultados de Q4 para justificar
#print(top_10_most_played_games_by_tag) #Resultados de Q3 para justificar
#print(mature_channel_tag) #Analisar tags com conteúdo promocional

with open('uniqueChannels.txt', 'w', encoding='utf-8') as arquivo:
    for channel in name_unique_channels:
        arquivo.write(f'{channel}\n')

games_eighteen_by_tag.to_excel('games18.xlsx')
mature_channel_tag.to_excel('promocionalTags.xlsx')
top_10_most_played_games_by_tag.to_excel('mostPlayed.xlsx')
top_viewers_df.to_excel('topviewer.xlsx')
frequencia_tags.to_excel('frequencia_tags_family_friendly.xlsx')

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
    'Canais com conteúdo promocional': count_mature_channel_by_tag,
    'Canais sem conteúdo promocional': count_not_mature_channel_by_tag
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

#Por hora
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_by_hour, x='Hour', y='Quantity', hue='Source URL', marker='o')

plt.title('Quantidade de Streams por Hora e por Tag')
plt.xlabel('Hora do Dia')
plt.ylabel('Quantidade de Streams')
plt.legend(title='Tag')
plt.grid(True)

# Adiciona todas as horas no eixo X
plt.xticks(np.arange(0, 24, 1))

plt.show()

#Por dia 
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_by_day, x='DayType', y='Quantity', hue='Source URL', marker='o')

plt.title('Quantidade de Streams por Tipo de Dia e por Tag')
plt.xlabel('Dia')
plt.ylabel('Quantidade de Streams')
plt.legend(title='Tag')
plt.grid(True)
plt.show()

#Por dia da semana
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_by_day_of_week, x='DayWeek', y='Quantity', hue='Source URL', marker='o')

plt.title('Quantidade de Streams por Dia da semana e por Tag')
plt.xlabel('Dia')
plt.ylabel('Quantidade de Streams')
plt.legend(title='Tag')
plt.grid(True)
plt.show()

#Média de audiência
plt.figure(figsize=(10, 6))
sns.barplot(data=average_audience, x='Source URL', y='Viewer Count')

plt.title('Média de Audiência por Tag')
plt.xlabel('Tag')
plt.ylabel('Média de Quantidade')
plt.grid(axis='y')
plt.show()
