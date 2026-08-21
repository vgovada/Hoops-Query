# FOR THE PURPOSE OF CHECKING HOW THEIR DATA IS FORMATTED

from nba_api.stats.endpoints import playergamelogs 

# Pulls in the player logs from the 23-24 season
logs = playergamelogs.PlayerGameLogs(season_nullable='2023-24')
# Pulls in the specific data frame (row)
df = logs.get_data_frames()[0]

# Prints how much data, column names, and the specific data itself
print(df.shape)
print(df.columns)
print(df.head())