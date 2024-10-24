from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

host = settings.DB_HOST
port = settings.DB_PORT
username = settings.DB_USERNAME
password = settings.DB_PASSWORD
database_name = settings.DB_DATABASE_NAME

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