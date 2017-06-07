import os
import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "postgres://ftujohlkcncztl:a82fe326ebb337fc39e8fbc5d56cf930721376914f4f87580109c7662a89b21b@ec2-174-129-224-33.compute-1.amazonaws.com:5432/dcv7gpiquaao08"
engine = sqlalchemy.create_engine(url)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


