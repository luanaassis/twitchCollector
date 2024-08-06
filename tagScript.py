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

df_final = pd.concat(dataframes, ignore_index=True)

count_mature_channels_by_tag = df_final['Classification Labels'].notnull().sum()
total_count_mature_channels = df_final[df_final['Classification Labels'].notnull()].groupby('Column_Name').size()
total_count_mature_games = df_final['Is Mature'].sum()
total_most_played_games = df_final['Game Name'].value_counts()
total_top_viewers = df.nlargest(10, 'Viewer Count')
total_count_eighteen = df_final['Age Rating'].str.contains(pattern, case=False, na=False).sum()

output_file = f'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\output_tag_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f'Count of Mature Channels: {total_count_mature_channels}\n')
    f.write(f'Count of Mature Games: {total_count_mature_games}\n')
    f.write('Most Played Games:\n')
    f.write(total_most_played_games.to_string())
    f.write('\n')
    f.write('Top Viewers:\n')
    f.write(total_top_viewers.to_string())
    f.write('\n')
    f.write(f'Count of Age Rating "eighteen", "18" or "CERO_Z": {total_count_eighteen}\n')
