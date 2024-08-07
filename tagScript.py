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

df_mid = pd.concat(dataframes, ignore_index=True)
df_final = df.drop_duplicates(subset=['Channel Id', 'Stream Title', 'Game ID'], keep='last')

total_count_mature_channels = df_final['Classification Labels'].notnull().sum()
count_mature_channels_by_tag = df_final[df_final['Classification Labels'].notnull()].groupby('Source URL').size()
total_count_mature_games = df_final['Is Mature'].sum()
count_mature_games_by_tag = df_final.groupby('Source URL')['Is Mature'].sum()
total_most_played_games = df_final['Game Name'].value_counts()
most_played_games_by_tag = df_final.groupby('Source URL')['Game Name'].value_counts()
total_top_viewers = df_final.nlargest(10, 'Viewer Count')
top_viewers_by_tag = df_final.groupby('Source URL').apply(lambda x: x.nlargest(10, 'Viewer Count')).reset_index(drop=True)
total_count_eighteen = df_final['Age Rating'].str.contains(pattern, case=False, na=False).sum()
count_eighteen_by_tag = df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False)].groupby('Source URL').size()
output_file = f'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\output_tag_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    # Total e proporção de canais maduros
    f.write(f"Total count of mature channels: {total_count_mature_channels}\n")
    for tag, count in count_mature_channels_by_tag.items():
        proportion = (count / total_count_mature_channels) * 100
        f.write(f"Tag: {tag}, Count: {count}, Proportion: {proportion:.2f}%\n")

    # Total e proporção de jogos maduros
    f.write(f"\nTotal count of mature games: {total_count_mature_games}\n")
    for tag, count in count_mature_games_by_tag.items():
        proportion = (count / total_count_mature_games) * 100
        f.write(f"Tag: {tag}, Count: {count}, Proportion: {proportion:.2f}%\n")

    # Total e proporção dos jogos mais jogados
    f.write(f"\nTotal most played games:\n{total_most_played_games}\n")
    for tag, counts in most_played_games_by_tag.groupby('Source URL'):
        f.write(f"\nTag: {tag}\n")
        f.write(f"{counts}\n")
        # Proporção não calculada aqui pois não há um total consolidado único

    # Total e proporção dos top visualizadores
    f.write(f"\nTotal top viewers:\n{total_top_viewers}\n")
    for tag, top_viewers in top_viewers_by_tag.groupby('Source URL'):
        f.write(f"\nTag: {tag}\n")
        f.write(f"{top_viewers}\n")
        # Proporção não calculada aqui pois não há um total consolidado único

    # Total e proporção de jogos com classificação 18
    f.write(f"\nTotal count of games rated 18: {total_count_eighteen}\n")
    for tag, count in count_eighteen_by_tag.items():
        proportion = (count / total_count_eighteen) * 100
        f.write(f"Tag: {tag}, Count: {count}, Proportion: {proportion:.2f}%\n")
