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

# Engine creation to link IDE and Postgres
password = quote_plus(os.getenv('DB_PASSWORD'))
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost:5432/hoops_query")

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

# Variable to give to the AI
question = "What was Lebron James's average points scored during the 23-24 season?"

# Exception message to feed into AI and self-correction loop check
exceptionPrompt = "No error to report, disregard this input."
exceptionBool = True
cap = 5

# Function for AI to generate SQL
def generateSQL(exceptionPrompt) :
    # Gives the AI the appropriate instructions to correctly output the optimized SQL
    prompt = f"""
        Instructions: I need you to craft the SQL query according to
        what you have in the schema and the question asked. The only technical things you need 
        to know are that seasons are formatted as yyyy-yy, date is yyyy-mm-dd, and all percentages 
        are in decimal format. Make your response perfectly clear so that I can copy and paste
        and the SQL server will read it, so no additional characters. 

        Finally, if the exception message given to you is an error, simply redo 
        your response with regards to the error given to you.

        SQL Schema: {schema}
        
        Question: {question}
        
        Exception message: {exceptionPrompt}
        """

    # AI takes prompt and responds with a SQL query
    ai_response = client.models.generate_content (
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # Cleans up the SQL AI response markdown text
    return ai_response.text.replace("```sql", "").replace("```", "")

# SQL Query generated
sql_query = generateSQL(exceptionPrompt)

# Self-Correction Loop to retry until response is valid or times-out
while (exceptionBool and cap > 0) :
    try :
        # Sending the AI SQL query to the database and returns the result
        result = pd.read_sql(sql_query, engine)

        # Checks to see if the result is NULL or invalid from Postgres
        if result.empty or result.isna().values.any() :
            print("Bad Result!")
            cap -= 1
            exceptionBool = True
            exceptionPrompt = f"""
                Postgres returned a NULL or invalid row/column. This means that
                the query is valid, however, is the wrong schema filter compared to the
                actual schema (Ex. Lebron James vs LeBron James). Recheck the schema and try again.

                Below you will find the original prompt and your response.
                Prompt: {question}
                Response: {sql_query}
                """
            sql_query = generateSQL(exceptionPrompt)
        else :
            # Breaks loop if no exception thrown
            exceptionBool = False
    except Exception as e:
        cap -= 1
        print(f"Attempt failed: {e}")
        exceptionPrompt = f"""
            Error found. The SQL Query given to PostGres generated an error. 
            Below is its response. 
            Error: {str(e)}

            Below is the prompt and your response. Retry your generation with regards to all
            three of these variables.
            Prompt: {question}
            Response: {sql_query}
            """
        sql_query = generateSQL(exceptionPrompt)

if exceptionBool:
    print("Your request timed out, it cannot be evaluated. Try something more simple.")
else:
    print(result)