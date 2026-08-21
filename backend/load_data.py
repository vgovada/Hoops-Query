# FOR THE PURPOSE OF LOADING ALL OF THE NECESSARY DATA INTO POSTGRE

from nba_api.stats.endpoints import playergamelogs 
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Loads the environment file into this file
load_dotenv()

# Creates a password variable that retrieves database password from .env and translates special characters as a viable pathway
password = quote_plus(os.getenv('DB_PASSWORD'))

# Creates the two-way connector bewteen postgres and python
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost:5432/hoops_query")
logs = playergamelogs.PlayerGameLogs(season_nullable='2023-24')
df = logs.get_data_frames()[0]

# The column list 
columns = {
    'SEASON_YEAR':        'season',
    'PLAYER_ID':          'player_id',
    'PLAYER_NAME':        'player_name',
    'TEAM_ABBREVIATION':  'team',
    'GAME_ID':            'game_id',
    'GAME_DATE':          'game_date',
    'MATCHUP':            'matchup',
    'WL':                 'win_loss',
    'MIN':                'minutes',
    'PTS':                'points',
    'OREB':               'off_rebounds',
    'DREB':               'def_rebounds',
    'AST':                'assists',
    'STL':                'steals',
    'BLK':                'blocks',
    'TOV':                'turnovers',
    'FGM':                'fgm',
    'FGA':                'fga',
    'FG_PCT':             'fg_pct',
    'FG3M':               'fg3m',
    'FG3A':               'fg3a',
    'FG3_PCT':            'fg3_pct',
    'FTM':                'ftm',
    'FTA':                'fta',
    'FT_PCT':             'ft_pct',
    'PLUS_MINUS':         'plus_minus',
}

# Creates a list of the keys from the columns list
columns_list = list(columns)

# Shortens the dataframe to those 25 columns using the keys
df = df[columns_list]

# Pushes the rename so that the new dataframe fully renames its list
df = df.rename(columns=columns)

# Date time needs to be specified first before translated to sql
df['game_date'] = pd.to_datetime(df['game_date'])

# Translates the dataframe to sql to push to postgresql
df.to_sql('player_games', con=engine, if_exists='replace', index=False)