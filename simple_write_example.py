import sqlalchemy
import os
import dotenv


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

event_name = input('What is the name of the event? ')

# Create a single connection to the database. Later we will discuss pooling connections.
conn = engine.connect()
conn.execute(
    sqlalchemy.text("INSERT INTO events (name) VALUES (:x)"),
    [{"x": event_name}],
)
# For DDL/DML statements, they need to be committed before they take effect.
# You can also turn on auto-commit with many libraries/drivers, but I suggest
# against doing so.
conn.commit()

# Read from the table to see the results of our run
result = conn.execute(sqlalchemy.text("SELECT * FROM events"))
for row in result:
    print(row)
