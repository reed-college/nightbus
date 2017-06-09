# We are using a flask library called passlib that lets us hash passwords we can switch to a different encryption scenario if the need
# arises. 

from datetime import datetime
from sqlalchemy import (Column, Boolean, Integer, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import database

# http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
Base = declarative_base()

### The schemas below are almost a direct copy from the http demo with a few tweaks. 
class IdPrimaryMixin(object):
    id = Column(Integer, primary_key=True)

class DateTimeMixin(object):
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# This class defines the database schema. That is it creates the model that is going to be followed by SQLAlchemy when creating the database.
# When we initially create the schema it will create a table called 'Users' and that table will have 10 columns called id, date created on, 
# date updated on, first name, last name, username, email and role. Maybe in the future once we figure out what our user authentication scheme
# will look like we can add an 11th column called passwords. So in short if we once we create the database and the table we can use this class
# to add and remove rows from the table. It is basically the same code as schema.py in Ross's http-demo example with three additional columns added.
# In addition to the table that is going to be created by the User class we need to create an Auth table that contains hashed passwords and username
class User(Base, IdPrimaryMixin, DateTimeMixin):
    __tablename__ = 'Users'

    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    username = Column(String(40), unique=True)
    email = Column(String(40))
    role = Column(String(20), unique=False)

    def __repr__(self):
        tpl = 'Person<id: {id}, {firstname} {lastname} {username} {email} {role}>'
        formatted = tpl.format(id=self.id, firstname=self.firstname, lastname=self.lastname, username=self.username, email=self.email, role=self.role)
        return formatted

# It is easier to authenticate users if we have a separate table that has all the usernames and passwords of all the users
# I still haven't figured out a way to populate one column in a table from an already existing column in another table. The idea is to automatically
# create a row in the Authentication table with the username from the Users table.
class Auth(Base, IdPrimaryMixin, DateTimeMixin):
    __tablename__ = 'Authentication'

    username = Column(String(40), unique = True)
    password = Column(String(128))
    # This was commented out because it was a hassle to have everyone confirm their email during development. But once we have ironed out all the details
    # for everything else we can de comment it. Also I'm not sure anymore about whether we need an email confirmation feature in our application.
    # confirmed = Column(Boolean, nullable = False, default = False)

    def encrypt_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

class Schedule(Base, IdPrimaryMixin):
    __tablename__ = 'schedule'

    day = Column(String(20))
    driver_id = Column(Integer)
    firstname = Column(String(20))
    lastname = Column(String(20))

        
# This creates all the tables that we have defined in our schema.py 
Base.metadata.create_all(database.engine)

