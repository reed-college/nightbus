from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import (Column, Integer, String,
                                DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

###### The next line is specific to my computer. In order to test the add driver page you have to set up a database on your own computer.
###### The format I used is 'postgresql://user:password@localhost/nameofdatabase'.

Base = declarative_base()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/nightbus'
db = SQLAlchemy(app)
engine = sqlalchemy.create_engine('postgresql://postgres@localhost/nightbus')

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)


class IdPrimaryMixin(object):
    id = Column(Integer, primary_key=True)

class DateTimeMixin(object):
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class User(Base, IdPrimaryMixin, DateTimeMixin):
    __tablename__ = 'Users'

    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    username = Column(String(40), unique=True)
    email = Column(String(40))
    role = Column(String(20), unique=False)

    def __repr__(self):
        tpl = 'Person<id: {id}, {firstname} {lastname} {username} {email} {role}>'
        formatted = tpl.format(id=self.id, firstname=self.firstname, lastname=self.lastname, email=self.email, role=self.role)
        return formatted

Base.metadata.create_all(db.engine)

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
    session = get_session()
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    email = request.form['email']
    new_driver = User(firstname=firstname, lastname=lastname, username=username, email=email)

    session.add(new_driver)
    session.commit()
    

    return "Driver successfully added"
        
@app.route('/remove')
def rmDriver():
    return render_template('remove.html')

if __name__ == '__main__':
        app.run()
