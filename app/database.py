from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import db_config

SQL_DATABASE_URI = f'postgresql://{db_config.postgres_username}:{db_config.postgres_password}@{db_config.postgres_hostname}:{db_config.postgres_port}/{db_config.postgres_dbname}'


#engine = create_engine(SQL_DATABASE_URI)

sessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

base = declarative_base()

def get_db():
  db = sessionLocal()
  try:
    yield db
  finally:
    db.close()




