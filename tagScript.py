import pandas as pd
import os
import datetime

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

#Metrics
unique_channels = df_final['Channel Id'].nunique()
unique_games = df_final['Game Name'].nunique()
count_mature_channels_by_tag = df_final[df_final['Classification Labels'].notnull()].groupby('Source URL').size()
count_mature_games_by_tag = df_final.groupby('Source URL')['Is Mature'].sum()
most_played_games_by_tag = df_final.groupby('Source URL')['Game Name'].value_counts()
most_played_games_by_tag = most_played_games_by_tag.reset_index(name='Count')
result_most_played_games_by_tag = pd.merge(most_played_games_by_tag, df_final[['Source URL','Stream Title', 'Game Name', 'Age Rating']], on=['Source URL', 'Game Name'], how='left')
top_viewers_by_tag = df_final.groupby('Source URL').apply(lambda x: x.nlargest(20, 'Viewer Count')).reset_index(drop=True)
colunas_desejadas = ['Source URL', 'Game Name', 'Viewer Count', 'Age Rating','Channel Name', 'Stream Title']
top_viewers_by_tag = top_viewers_by_tag[colunas_desejadas]
top_viewers_by_tag['Age Rating Flag'] = top_viewers_by_tag['Age Rating'].str.contains(pattern).astype(int)
count_eighteen_by_tag = df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False)].groupby('Source URL').size()

output_file = f'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\output_tag_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('Quantos canais classificados como adultos fazem streams e colocam tags relacionadas ao público infantil?:\n' )
    for tag, count in count_mature_channels_by_tag.items():
        proportion = (count / unique_channels) * 100
        f.write(f"Tag: {tag}, Count: {count}, Total:{unique_channels}, Proportion: {proportion:.2f}%\n")
    f.write('Quantos jogos com classificaçao indicativa 18 sao exibidos em lives com tags que estao relacionadas ao publico infantil? (CLASSIFICADA PELO STREAMER):\n')
    for tag, count in count_mature_games_by_tag.items():
        proportion = (count / unique_games) * 100
        f.write(f"Tag: {tag}, Count: {count}, Total:{unique_games},Proportion: {proportion:.2f}%\n")
    f.write('Quantos jogos com classificaçao indicativa 18 sao exibidos em lives com tags que estao relacionadas ao publico infantil? (CLASSIFICADA PELO IGDB):\n')
    for tag, count in count_eighteen_by_tag.items():
        proportion = (count / unique_games) * 100
        f.write(f"Tag: {tag}, Count: {count}, Total:{unique_games}, Proportion: {proportion:.2f}%\n")
    f.write('Quais os jogos mais jogados com as tags relacionadas ao publico infantil? \n')
    f.write(f"{result_most_played_games_by_tag}\n")
    f.write('Os conteudos mais visualizados sao de conteUdos apropriados ao publico infantil?:\n')
    f.write(f"\n{top_viewers_by_tag}\n")
