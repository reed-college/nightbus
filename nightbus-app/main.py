from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sds:chickencombo@localhost/nightbus'
db = SQLAlchemy(app)

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def home():
    return 'Home Page'

@app.route('/rider')
def rider():
    return 'Riders Page'

@app.route('/driver')
def driver():
    return 'Drivers Page'

@app.route('/admin')
def admin():
    return 'Admins Page'

@app.route('/add')
def addDriver():
    return 'Add Drivers Page'

@app.route('/remove')
def rmDriver():
    return 'Remove Drivers Page'

if __name__ == '__main__':
        app.run()
