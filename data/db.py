import os 
import sys 
from pathlib import Path 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

db_url = os.environ['CRYPTID_SQLITE_DB']
engine = create_engine(str(db_url), echo = True)
Session = sessionmaker(engine)

@contextmanager
def get_session():
    session = Session()

    try:
        yield session
    finally:
        session.close()