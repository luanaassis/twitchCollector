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

count_mature_channels = df_final['Classification Labels'].notnull().sum()
count_mature_games = df_final['Is Mature'].sum()
most_played_games = df_final['Game Name'].value_counts()
top_viewers = df.nlargest(10, 'Viewer Count')
count_eighteen = df_final['Age Rating'].str.contains(pattern, case=False, na=False).sum()

print(count_mature_channels)
print(count_mature_games)
print(most_played_games)
print(top_viewers)
print(count_eighteen)

output_file = f'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\output_tag_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f'Count of Mature Channels: {count_mature_channels}\n')
    f.write(f'Count of Mature Games: {count_mature_games}\n')
    f.write('Most Played Games:\n')
    f.write(most_played_games.to_string())
    f.write('\n')
    f.write('Top Viewers:\n')
    f.write(top_viewers.to_string())
    f.write('\n')
    f.write(f'Count of Age Rating "eighteen", "18" or "CERO_Z": {count_eighteen}\n')
