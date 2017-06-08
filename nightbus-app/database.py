import os
import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = os.environ.get('DATABASE_URL')
engine = sqlalchemy.create_engine(url)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


