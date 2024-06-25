import pandas as pd
import os

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