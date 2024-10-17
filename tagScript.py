import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re

folder = 'C:\\Users\\luana\\Desktop\\twitchCollector-dev\\apresentacao\\tags'
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
    'https://www.twitch.tv/directory/all/tags/kidstream':'kidstream',
    'https://www.twitch.tv/directory/all/tags/SFW': 'SFW',
    'https://www.twitch.tv/directory/all/tags/SafeSpace': 'SafeSpace' 
     })
tags = ['FamilyFriendly','Kids','Kid','KidStreaming','KidSafe','KidFriendly','KidGamer','Childrens','KidsGaming','ChildFriendlyStream',
        'KidsAndParentsGamers','KidShow','Friendly','Family','KidsFriendly','KIDSTREAMER','kidstream','SFW','SafeSpace']

df_final = df_final[df_final['Source URL'] != 'https://www.twitch.tv/directory/all/tags/gamble']
df_final = df_final[df_final['Source URL'] != 'https://www.twitch.tv/directory/all/tags/gambling']
df_final['SearchTime'] = pd.to_datetime(df_final['SearchTime'])
df_final['Hour'] = df_final['SearchTime'].dt.hour
df_final['DayType'] = df_final['SearchTime'].dt.weekday.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
df_final['DayWeek'] = df_final['SearchTime'].dt.day_name()
df_final['Viewer Count'] = pd.to_numeric(df_final['Viewer Count'], errors='coerce')

pattern = '|'.join(tags)
tags_in_same_stream = df_final[df_final['Stream Tags'].str.count(pattern) > 1]

title_in_same_stream = df_final[df_final['Stream Title'].str.contains(pattern, na=False)]

#Metrics
tags_from_family_friendly = df_final.loc[df_final['Source URL'] == 'FamilyFriendly', 'Stream Tags']
todas_as_tags = tags_from_family_friendly.str.split(', ').explode()
frequencia_tags = todas_as_tags.value_counts()

north_american_pattern = df_final[
    df_final['Classification Labels'].str.contains('MatureGame') &
    df_final['Age Rating'].str.contains(r"\('ESRB', 'M'\)")
]

count_north_american_pattern = df_final[
    df_final['Classification Labels'].str.contains('MatureGame') &
    df_final['Age Rating'].str.contains(r"\('ESRB', 'M'\)")
].shape[0]  # Contar as ocorrências

euro_pattern = df_final[
    df_final['Classification Labels'].str.contains('MatureGame') &
    df_final['Age Rating'].str.contains(r"\('PEGI', 'Eighteen'\)")
]

count_euro_pattern = df_final[
    df_final['Classification Labels'].str.contains('MatureGame') &
    df_final['Age Rating'].str.contains(r"\('PEGI', 'Eighteen'\)")
].shape[0]  # Contar as ocorrências

BR_pattern = df_final[
    df_final['Classification Labels'].str.contains('MatureGame') &
    df_final['Age Rating'].str.contains('CLASS_IND_Eighteen')
]

count_BR_pattern = df_final[
    df_final['Classification Labels'].str.contains('MatureGame') &
    df_final['Age Rating'].str.contains('CLASS_IND_Eighteen')
].shape[0]  # Contar as ocorrências

count_only_BR_pattern = df_final[
    df_final['Age Rating'].str.contains('CLASS_IND_Eighteen') &
    ~df_final['Classification Labels'].fillna('').str.contains('MatureGame')
].shape[0]  # Contar as ocorrências

df_diff_patterns_BR = df_final[df_final['Age Rating'].str.contains('CLASS_IND_Eighteen') & ~df_final['Classification Labels'].fillna('').str.contains('MatureGame')]
df_diff_patterns_BR.to_excel('pattern_BR_DIFF.xlsx')

df_diff_patterns_euro = df_final[df_final['Age Rating'].str.contains(r"\('PEGI', 'Eighteen'\)") & ~df_final['Classification Labels'].fillna('').str.contains('MatureGame')]
df_diff_patterns_euro.to_excel('pattern_EURO_DIFF.xlsx')

df_diff_patterns_usa = df_final[df_final['Age Rating'].str.contains(r"\('ESRB', 'M'\)") & ~df_final['Classification Labels'].fillna('').str.contains('MatureGame')]
df_diff_patterns_usa.to_excel('pattern_USA_DIFF.xlsx')

total_pattern = df_final[df_final['Classification Labels'].str.contains('MatureGame', na=False)]
count_total_pattern = df_final['Classification Labels'].str.contains('MatureGame', na=False).sum()

data_patternn = {
    'Region': ['North America', 'Europe', 'Brazil', 'Total'],
    'Pattern Count': [count_north_american_pattern, count_euro_pattern, count_BR_pattern, count_total_pattern]
}
df_patterns = pd.DataFrame(data_patternn)
df_patterns.to_excel('patterns_summary.xlsx', index=False)

language_counts = df_final.groupby(['Language', 'Source URL'])['Channel Name'].nunique().reset_index(name='Unique Channel Count')

mature_channel = df_final[df_final['Is Mature'] == 1]
mature_channel_tag = mature_channel[['Stream Tags', 'Source URL']]
todas_as_tags_promocionais = mature_channel_tag['Stream Tags'].str.split(', ').explode()
frequencia_tags_promocionais = todas_as_tags_promocionais.value_counts().reset_index(name='Quantity')

mature_channel_analisys = mature_channel[mature_channel['Stream Tags'].str.contains('ADHD') | mature_channel['Stream Tags'].str.contains('Chill')]
mature_channel_analisys.to_excel('mature_analisys.xlsx')

grouped_by_hour = df_final[['Hour', 'Source URL']]
grouped_by_hour = grouped_by_hour.groupby(['Hour', 'Source URL']).size().reset_index(name='Quantity')
average_by_hour = grouped_by_hour.groupby(['Hour', 'Source URL'])['Quantity'].mean().reset_index(name='Average_Quantity')

grouped_by_hour_language = df_final[['Hour','Language','Source URL']]
grouped_by_hour_language = grouped_by_hour_language.groupby(['Hour','Language','Source URL']).size().reset_index(name='Quantity')
total_by_language = grouped_by_hour_language.groupby('Language')['Quantity'].sum().reset_index()
top_5_languages = total_by_language.sort_values(by='Quantity', ascending=False).head(5)
if 'pt' not in top_5_languages['Language'].values:
    pt_row = total_by_language[total_by_language['Language'] == 'pt']
    top_5_languages = pd.concat([top_5_languages, pt_row])
grouped_by_top_languages = grouped_by_hour_language[grouped_by_hour_language['Language'].isin(top_5_languages['Language'])]

def adjust_quantity(row):
    if row['DayType'] == 'Weekday':
        return row['Quantity'] / 5
    elif row['DayType'] == 'Weekend':
        return row['Quantity'] / 2

grouped_by_day = df_final[['DayType', 'Source URL']]
grouped_by_day = grouped_by_day.groupby(['DayType', 'Source URL']).size().reset_index(name='Quantity')
grouped_by_day['Adjusted_Quantity'] = grouped_by_day.apply(adjust_quantity, axis=1)

grouped_by_day_of_week = df_final[['DayWeek', 'Source URL']]
grouped_by_day_of_week = grouped_by_day_of_week.groupby(['DayWeek', 'Source URL']).size().reset_index(name='Quantity')
grouped_by_day_of_week = grouped_by_day_of_week.groupby(['DayWeek', 'Source URL'])['Quantity'].mean().reset_index(name='Average_Quantity')
order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
grouped_by_day_of_week['DayWeek'] = pd.Categorical(grouped_by_day_of_week['DayWeek'], categories=order_days, ordered=True)
grouped_by_day_of_week = grouped_by_day_of_week.sort_values('DayWeek')

name_unique_channels = df_final.groupby('Source URL')['Channel Name'].unique()
qty_unique_channels = df_final[['Channel Name', 'Source URL']]
qty_unique_channels.drop_duplicates(subset=['Channel Name', 'Source URL'], keep='last')
unique_games = df_final.groupby('Source URL')['Game Name'].nunique()

count_mature_classification_by_tag = df_final[df_final['Classification Labels'].notnull()].groupby('Source URL').size()
count_not_mature_classification_by_tag = df_final[df_final['Classification Labels'].isnull()].groupby('Source URL').size()

count_mature_channel_by_tag = df_final[df_final['Is Mature'] == 1].groupby('Source URL').size()
count_not_mature_channel_by_tag = df_final[df_final['Is Mature'] == 0].groupby('Source URL').size()

channels_eighteen =  df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False) | df_final['Classification Labels'].str.contains('MatureGame', case=False, na=False)].groupby('Channel Name').size()

count_eighteen_by_tag = df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False) | df_final['Classification Labels'].str.contains('MatureGame', case=False, na=False)].groupby('Source URL').size()
count_not_eighteen_by_tag = df_final[~df_final['Age Rating'].str.contains(pattern, case=False, na=False)| ~df_final['Classification Labels'].str.contains('MatureGame', case=False, na=False)].groupby('Source URL').size()

top_viewers_df = (
    df_final.groupby('Source URL')
    .apply(lambda x: x.nlargest(10, 'Viewer Count'))
    .reset_index(drop=True))
top_viewers_df['Age Ratings Indicator'] = (top_viewers_df['Age Rating'].str.contains(pattern)| top_viewers_df['Classification Labels'].str.contains('MatureGame', case=False, na=False)).astype(int)
counts_top_viewers = top_viewers_df.groupby('Source URL')['Age Ratings Indicator'].value_counts().unstack(fill_value=0)

most_played_games_by_tag = df_final.groupby('Source URL')['Game Name'].value_counts()
most_played_games_by_tag = most_played_games_by_tag.reset_index(name='Count')
result_most_played_games_by_tag = pd.merge(most_played_games_by_tag, df_final[['Source URL', 'Game Name', 'Age Rating']], on=['Source URL', 'Game Name'], how='left')
result_most_played_games_by_tag = result_most_played_games_by_tag.drop_duplicates(subset=['Source URL', 'Game Name'])
result_most_played_games_by_tag['Age Ratings Indicator'] = (result_most_played_games_by_tag['Age Rating'].str.contains(pattern).astype(int))
counts_popular_games = top_viewers_df.groupby('Source URL')['Age Ratings Indicator'].value_counts()

top_10_most_played_games_by_tag = result_most_played_games_by_tag.groupby('Source URL').apply(lambda x: x.nlargest(10, 'Count'))
top_10_most_played_games_by_tag = top_10_most_played_games_by_tag.reset_index(drop=True)

games_eighteen_by_tag = df_final[df_final['Age Rating'].str.contains(pattern, case=False, na=False)| df_final['Classification Labels'].str.contains('MatureGame', case=False, na=False)][['Source URL', 'Game Name', 'IGDB ID']].drop_duplicates()
games_not_eighteen_by_tag = df_final[
    ~df_final['Classification Labels'].str.contains('MatureGame', case=False, na=False)
][['Source URL', 'Game Name', 'IGDB ID']].drop_duplicates()
average_audience = df_final.groupby('Source URL')['Viewer Count'].mean().reset_index()
#print(name_unique_channels) #Nome dos canais buscados
#print(games_eighteen_by_tag) #Diferentes jogos +18
#print(top_viewers_df) #Resultados de Q4 para justificar
#print(top_10_most_played_games_by_tag) #Resultados de Q3 para justificar
#print(mature_channel_tag) #Analisar tags com conteúdo promocional
qty_unique_channels.to_excel('QTYcanaisUnicos.xlsx')
name_unique_channels.to_excel('canaisUnicos.xlsx')
games_eighteen_by_tag.to_excel('games18.xlsx')
games_not_eighteen_by_tag.to_excel('not18games.xlsx')
mature_channel_tag.to_excel('promocionalTags.xlsx')
top_10_most_played_games_by_tag.to_excel('mostPlayed.xlsx')
top_viewers_df.to_excel('topviewer.xlsx')
frequencia_tags.to_excel('frequencia_tags_family_friendly.xlsx')
frequencia_tags_promocionais.to_excel('frequencia_tags_promocionais.xlsx')
channels_eighteen.to_excel('canais_18.xlsx')
tags_in_same_stream.to_excel('tags_same_stream.xlsx')
title_in_same_stream.to_excel('title_with_tag.xlsx')
df_final.to_excel("final.xlsx")
result_most_played_games_by_tag.to_excel('most_played_games.xlsx')

df_age_description = pd.read_excel('games18PQ.xlsx')

def extract_descriptions(details_str):
    # Usa expressão regular para extrair todas as descrições
    descriptions = re.findall(r"'description': '([^']*)'", details_str)
    # Retorna as descrições encontradas
    return descriptions

# Aplica a função à coluna 'details' e cria uma nova coluna 'descriptions'
df_age_description['descriptions'] = df_age_description['Age Rating Description'].apply(extract_descriptions)
df_age_description = df_age_description.drop(['Unnamed: 0.1', 'Unnamed: 0','Game Name','IGDB ID','Age Rating Description'], axis=1)
df_age_description = df_age_description.explode('descriptions')
df_age_description['descriptions'] = df_age_description['descriptions'].replace({
    'Conteúdo Sexual (Sexual Content)': 'Sexual Content',
    'Drogas (Drugs)' : 'Drugs',
    'Drogas Ilícitas (Illegal Drugs)' : 'Illegal Drugs',
    'Drogas Lícitas (Legal Drugs)' : 'Legal Drugs',
    'Linguagem Imprópria (Inappropriate Language)' : 'Inappropriate Language',
    'Nudez (Nudity)' : 'Nudity',
    'Violência (Violence)' : 'Violence',
    'Violência Extrema (Extreme Violence)' : 'Extreme Violence'})
df_age_description = df_age_description.reset_index()
df_age_description = df_age_description.drop_duplicates()
df_age_description = df_age_description.groupby('Source URL')['descriptions'].value_counts().unstack(fill_value=0)
df_age_description.to_excel('age_description.xlsx')

df_age = pd.read_excel('age_description.xlsx')

def make_radar_chart(df, categories):
    # Número de variáveis
    num_vars = len(categories)

    # Calcula o ângulo de cada eixo em um gráfico de radar
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Adiciona o ângulo do ponto de início para completar o círculo
    angles += angles[:1]

    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    # Repetir para cada linha (cada "Source URL")
    for i, row in df.iterrows():
        values = row[1:].values.flatten().tolist()  # Pega todos os valores exceto o primeiro
        values += values[:1]  # Completa o ciclo para o gráfico de radar

        # Verifica se os valores são numéricos
        values = [float(v) for v in values]  # Converte para float, se necessário

        # Desenha a linha de cada 'Source URL'
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=str(row['Source URL']))
        ax.fill(angles, values, alpha=0.1)  # Preenche a área

    # Adiciona as labels nas categorias
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Exibe a legenda
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.title("Gráfico de Radar - Descritores por Source URL")
    plt.show()

# Defina as categorias que correspondem às colunas da tabela, exceto 'Source URL'
categories = list(df_age.columns[1:])
print(list(df_age.columns[0]))

# Chame a função para desenhar o gráfico de radar
make_radar_chart(df_age, categories)

plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_by_top_languages, x='Hour', y='Quantity', hue='Language', marker='o')
plt.title('Quantidade ao Longo das Horas por Linguagem')
plt.xticks(rotation=45)
plt.tight_layout()
plt.xticks(np.arange(0, 24, 1))
plt.show()

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
ax.set_title('Comparação entre Contagem de Streams com Jogos Adultos e Jogos Não Adultos por TAG')
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
sns.lineplot(data=average_by_hour, x='Hour', y='Average_Quantity', hue='Source URL', marker='o')

plt.title('Média de Streams por Hora e por Tag')
plt.xlabel('Hora do Dia')
plt.ylabel('Quantidade Média de Streams')
plt.legend(title='Tag')
plt.grid(True)

# Adiciona todas as horas no eixo X
plt.xticks(np.arange(0, 24, 1))

plt.show()


#Por dia 
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_by_day, x='DayType', y='Adjusted_Quantity', hue='Source URL', marker='o')

plt.title('Média de Streams por Tipo de Dia e por Tag')
plt.xlabel('Dia')
plt.ylabel('Quantidade Média de Streams')
plt.legend(title='Tag')
plt.grid(True)
plt.show()

#Por dia da semana
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_by_day_of_week, x='DayWeek', y='Average_Quantity', hue='Source URL', marker='o')

plt.title('Média de Streams por Dia da semana e por Tag')
plt.xlabel('Dia')
plt.ylabel('Quantidade Média de Streams')
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