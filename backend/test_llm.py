# GETS THE AI TO RECEIVE INPUT, TURN INTO SQL QUERY, THEN GIVE BACK SQL DATA

from google import genai
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import os
from urllib.parse import quote_plus

# Loads the environment file into this file
load_dotenv()

# Creates a password variable that retrieves API key from .env
apiKey = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=apiKey)

# Variable to give to the AI
question = "What was Lebron James's average points scored during the 23-24 season?"

schema = """
Table: player_games
    Columns:
        season (text), 
        player_id (bigint), 
        player_name (text),
        team (text),
        game_id (text),
        game_date (timestamp without time zone),
        matchup (text),
        win_loss (text),
        minutes (double precision),
        points (bigint),
        off_rebounds (bigint),
        def_rebounds (bigint),
        assists (bigint),
        steals (bigint),
        blocks (bigint),
        turnovers (bigint),
        fgm (bigint),
        fga (bigint),
        fg_pct (double precision),
        fg3m (bigint),
        fg3a (bigint),
        fg3_pct (double precision),
        ftm (bigint),
        fta (bigint),
        ft_pct (double precision),
        plus_minus (bigint)
"""

# Gives the AI the appropriate instructions to correctly output the optimized SQL
prompt = f"""
    Instructions: I need you to craft the SQL query according to
    what you have in the schema and the question asked. The only technical things you need 
    to know are that seasons are formatted as yyyy-yy, date is yyyy-mm-dd, and all percentages 
    are in decimal format. Make your response perfectly clear so that I can copy and paste
    and the SQL server will read it, so no additional characters.

    SQL Schema: {schema}
    
    Question: {question}"""

# AI takes prompt and responds with a SQL query
ai_response = client.models.generate_content (
    model="gemini-3.5-flash-lite",
    contents=prompt
)

# Cleans up the SQL AI response markdown text
sql_query = ai_response.text.replace("```sql", "").replace("```", "")

# Engine creation to link IDE and Postgres
password = quote_plus(os.getenv('DB_PASSWORD'))
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost:5432/hoops_query")

# Sending the AI SQL query to the database and returns the result
result = pd.read_sql(sql_query, engine)

print(result)