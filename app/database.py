from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_DATABASE_URI = 'postgresql://postgres@localhost/fastapi_test'

engine = create_engine(SQL_DATABASE_URI)

sessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

base = declarative_base()

def get_db():
  db = sessionLocal()
  try:
    yield db
  finally:
    db.close()




