from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url())

# Create a single connection to the database. Later we will discuss pooling connections.
conn = engine.connect()

# The sql we want to execute
sql = """
SELECT year, cause_name, SUM(deaths) AS total_deaths
FROM leading_cause_of_death
GROUP BY year, cause_name
ORDER BY year, total_deaths DESC
"""

# Run the sql and returns a CursorResult object which represents the SQL results
result = conn.execute(sqlalchemy.text(sql))

# Iterate over the CursorResult object row by row and just print.
# In a real application you would access the fields directly.
for row in result:
    print(row)
