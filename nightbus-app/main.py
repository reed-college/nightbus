from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)

###### The next line is specific to my computer. In order to test the add driver page you have to set up a database on your own computer.
###### The format I used is 'postgresql://user:password@localhost/nameofdatabase'.


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sds:chickencombo@localhost/nightbus'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    username = request.form['username']
    email = request.form['email']
    new_driver = User(username, email)
    db.session.add(new_driver)
    db.session.commit()

    return "Driver successfully added"
        
@app.route('/remove')
def rmDriver():
    return render_template('remove.html')

if __name__ == '__main__':
        app.run()
