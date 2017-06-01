# The datetime module allows us to find the exact time right now automatically. It was imported to record when a user was created and if any changes
# have been made to the user to record the date the modification was made.
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
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


# Since we can't store passwords as they are in a database we need to use some sort of encryption tool. I chose to use passlib because it was already
# available and easy to use with our schema

from passlib.apps import custom_app_context as pwd_context

from flask_httpauth import HTTPBasicAuth

from functools import wraps

# The next three imports don't do anything. I imported them when I was trying to set up migrations and user authentication which I couldn't get done.
#from flask_login import LoginManager
#from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.secret_key = 'This is secret'
auth = HTTPBasicAuth()

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
class Auth(Base, IdPrimaryMixin, DateTimeMixin):
    __tablename__ = 'Authentication'

    username = Column(String(40), unique = True)
    password = Column(String(128))

    def encrypt_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
        

# I honestly don't know why I added this line but the add user page seemed to work without it on my machine so if anyone gets an error with SQLAlchemy this 
# could be it. I think this line was here to create all schemas when we were using flask's own sqlalchemy and it doesn't work with the normal sqlalchemy
#Base.metadata.create_all(engine)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if session['logged_in']:
            print('This actually runs')
            return test(*args, **kwargs)
        else:
            flash('You need to log in first')
            return redirect(url_for('login'))
    return wrap



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rider')
@login_required
def rider():
    return render_template('rider.html')

@app.route('/driver')
def driver():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('driver.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('admin.html')

@app.route('/add')
def addDriver():
    return render_template('add.html')

@app.route('/adduser', methods=['POST'])
def addUser():
    # create a session or a connection to the nightbus database
    db_session = get_session()

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
    db_session.add(new_driver)
    db_session.commit()

    # To check if a user has been successfully added to the database open a new tab in terminal, use the command psql nightbus to go to the nightbus database and do 
    # SELECT * FROM "Users"; and it should be the last entry in that table.
    # Most of the stuff related to the databases I found at https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/ and http-demo
    

    return "Driver successfully added"
        
@app.route('/remove')
def rmDriver():
    return render_template('remove.html')

@app.route('/removeuser', methods=['POST'])
def removeUser():
    # This function is basically identical to the user addition function. We use the get_session method to create a connection with the database. Next we get the value of the username
    # that was entered in the form using the request library that comes with flask.
    db_session = get_session()
    username = request.form['username']

    # Next we use the query method to search the table User and we filter our query by the username we got above. This displays the first entry it gets so I don't know how we would handle
    # two different people having two different user names. More documentation on querying and just general sqlalchemy knowledge can be found at http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying
    # After that we just use the built in delete method to remove the user and then we have to make sure we commit after that to make the deletion permanent.
    user = db_session.query(User).filter_by(username=username).first()
    db_session.delete(user)
    db_session.commit()

    return "user successfully removed"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['GET','POST'])
def register():
    # this function should allow anyone to register and be able to log in right now. Once we have that we can work on different views for different types of users and stuff like that.
    # it works in similar fashion like the add driver and remove driver functions it connects to the databases using the get session function and gets the data from the form using the
    # flask request module then it creates a User and an Auth entry. The user entry is just for keeping track of users while the auth entry will contain the username and the password
    # the person signed up with. We don't actually store the password we encrypt it using the passlib library that we imported above. We then add both entries to their respective
    # tables and we commit and then we are done.
    db_session = get_session()

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = User(firstname = firstname, lastname = lastname, email = email, username = username, role=role)
    user_auth = Auth(username=username)
    user_auth.encrypt_password(password)

    db_session.add(user)
    db_session.add(user_auth)
    db_session.commit()

    return "User successfully registered"

@app.route('/login', methods=['GET', 'POST'])
def login():
    # This is the route you should go to in order to test if login works. You have to sign up using the registration page before you can log in. Our next step should be trying to
    # figure out how to make things visible only for certain users and all that stuff.
    return render_template('login.html')


@app.route('/validate_credentials', methods=['GET', 'POST'])
def validate_credentials():
    # This function asks for a username and a password and it queries the database for that username and uses the predefined verify_password method to log you in or not log you in.
    db_session = get_session()
    username = request.form['username']
    password = request.form['password']

    user_auth = db_session.query(Auth).filter_by(username=username).first()
    user_role = db_session.query(User).filter_by(username=username).first()

    if user_auth.verify_password(password):
        session['logged_in'] = True
        if user_role.role == 'Admin':
            return redirect(url_for('admin'))
        elif user_role.role == 'Driver':
            return redirect(url_for('driver'))
        else:
            return redirect(url_for('login'))
    else:
        flash('Invalid Credentials')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect (url_for('home'))



if __name__ == '__main__':
        app.run()
