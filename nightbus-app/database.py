import os
import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "postgres://pakqjossssuvfz:b6d2cf54195a2103c58a1026e3b8a5c3abe6461491e4b534ef8b29963219387e@ec2-50-17-236-15.compute-1.amazonaws.com:5432/dfaectjl5ak2mm"
#url = "postgresql://postgres@localhost/nightbus"
engine = sqlalchemy.create_engine(url)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


