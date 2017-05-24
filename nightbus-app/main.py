from flask import Flask, render_template
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

@app.route('/remove')
def rmDriver():
    return render_template('remove.html')

if __name__ == '__main__':
        app.run()
