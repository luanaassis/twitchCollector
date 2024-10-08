import pandas as pd
import os
import matplotlib.pyplot as plt

folder = 'C:\\Users\\luana\\Desktop\\twitchCollector-dev'
files = [f for f in os.listdir(folder) if f.endswith('.xlsx') and f.startswith('twitch_data_tags')]

dataframes = []
pattern = r'\b(?:eighteen|18|CERO_Z)\b'

for file in files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path, engine='openpyxl')
    print(file)
    dataframes.append(df)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)
df_final = pd.concat(dataframes, ignore_index=True)
df_final = df_final.drop_duplicates(subset=['Channel Id','Channel Name','Stream Title', 'Game ID', 'Source URL'])

#Metrics
unique_channels = df_final.groupby('Source URL')['Channel Id'].nunique()
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
counts_popular_games = top_viewers_df.groupby('Source URL')['Age Ratings Indicator'].value_counts().unstack(fill_value=0)

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
ax.set_title('Comparação entre Contagem de Canais Adultos e Canais Não Adultos por TAG')
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
fig, ax = plt.subplots(figsize=(12, 6))
counts_top_viewers.plot(kind='bar', stacked=True, color=colors, ax=ax)
plt.title('Classificação dos jogos exibidos nas streams mais visualizadas por Tag')
plt.xlabel('Tag')
plt.ylabel('Quantidade')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Fifth graph
colors = ['#0000ff','#ff0000']
fig, ax = plt.subplots(figsize=(12, 6))
counts_popular_games.plot(kind='bar', stacked=True, color=colors, ax=ax)
plt.title('Classificação dos jogos mais exibidos nas streams por Tag')
plt.xlabel('Tag')
plt.ylabel('Quantidade')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
