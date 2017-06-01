import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('postgresql://postgres@localhost/nightbus')

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


