import os
import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "postgres://tfnvyxrzzrtvoo:65dca5bab62b3de57c34f88f53633b0ceb74d70f8aa16f664b0431ed4d316b6f@ec2-107-22-162-158.compute-1.amazonaws.com:5432/d9fijolsgb73g8"
engine = sqlalchemy.create_engine(url)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


