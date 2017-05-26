# The datetime module allows us to find the exact time right now automatically. It was imported to record when a user was created and if any changes
# have been made to the user to record the date the modification was made.
from datetime import datetime
from flask import Flask, render_template, request
# commented the next import out because 1) that's what ross did and 2) it caused a lot of errors when the flask sqlalchemy mixed with the standalone
# sqlalchemy
#from flask_sqlalchemy import SQLAlchemy
#
#
import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# The next three imports don't do anything. I imported them when I was trying to set up migrations and user authentication which I couldn't get done.
#from flask_login import LoginManager
#from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)


# http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
Base = declarative_base()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/nightbus'
#db = SQLAlchemy(app)
# This line creates an engine or a starting base for sqlalchemy. It tells sqlalchemy what the dialect(type) of sql we are using and where to look for it
# on the local machine.
engine = sqlalchemy.create_engine('postgresql://postgres@localhost/nightbus')


# The get_session function creates a connection with the database if given a valid engine or starting point. In short if the above line didn't return any 
# errors the database has been found and we can connect to it using sqlalchemy's orm own sessionmaker. 
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

#migrate = Migrate(app, db)


# The next four lines can be uncommented by anyone who wants to work on database migration and user authentication. I got them from the Flask-Login and
# Flask-Migrate Documentations online (which can be found at https://flask-login.readthedocs.io/en/latest/ and https://flask-migrate.readthedocs.io/en/latest/)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

#login_manager = LoginManager()
#login_manager.init_app(app)


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

# I honestly don't know why I added this line but the add user page seemed to work without it on my machine so if anyone gets an error with SQLAlchemy this 
# could be it.
#Base.metadata.create_all(db.engine)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rider')
def rider():
    return render_template('rider.html')

@app.route('/driver')
def driver():
    return render_template('driver.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add')
def addDriver():
    return render_template('add.html')

@app.route('/newdriver', methods=['POST'])
def newDriver():
    # create a session or a connection to the nightbus database
    session = get_session()

    # Using http request method we can get information from html elements by using the request library in python. Give any html element a name and an action associated with that
    # name for example <form action='\newdriver method=post> and if the form has an element called Name: <input type="text" name="name" we can get the form to send the value of 
    # name entered using the post method and we can get it on the python end by doing request.form['name'] and since the form has an action called '\newdriver the server will know
    # and run whichever function is below the @app.route('/newdriver) line
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    email = request.form['email']
    role = request.form['role']

    # Using the schema we created above we can enter the data we got into the database. Also another copy from http-demo and can be found in line 82 of the http-demo
    new_driver = User(firstname=firstname, lastname=lastname, username=username, email=email, role=role)


    # Add the new driver we defined above to the database using the built in method 'add' and once again using the built in method 'commit' make sure the record is permanently
    # entered into the databse.
    session.add(new_driver)
    session.commit()

    # To check if a user has been successfully added to the database open a new tab in terminal, use the command psql nightbus to go to the nightbus database and do 
    # SELECT * FROM "Users"; and it should be the last entry in that table.
    # Most of the stuff related to the databases I found at https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/ and http-demo
    

    return "Driver successfully added"
        
@app.route('/remove')
def rmDriver():
    return render_template('remove.html')

if __name__ == '__main__':
        app.run()
