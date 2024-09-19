from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

username = "postgres"
password = "mohan"
host = "localhost"
port = "5432"
database_name = "python_learning"

# Create an engine connected to the Postgres database
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Base class for our classes definitions
Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()