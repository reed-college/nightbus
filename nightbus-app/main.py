import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from decorators import login_required
from flask_mail import Message, Mail
from user_handling import generate_confirmation_token, confirm_email_token, send_mail
from itsdangerous import URLSafeTimedSerializer
import config
import schema
import database
import post_to_fb

#from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)
mail = Mail()

# I created a class that has all the configurations we need for the app to run. If we want to change the configuration or when we have to finally deploy the app
# we can just create another class called ProdConfig with the appropriate attributes. This wasn't necessary at this point but the main.py was getting messy.
app.config.from_object('config.TestConfig')
mail.init_app(app)

# We need to generate a unique token everytime a user registers to confirm their email. We use the URLSafeTimedSerializer serializer from the it's dangerous module.
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


#update bus statuses upon hitting buttons on driver page

status = "here"

class NightBus:
    def __init__(self):
        self.current_status = status
    def get_current_status(self):
        return self.current_status
    def update_status(self,new_status):
        self.current_status = new_status

b  = NightBus()

@app.route('/update_state/')
def update_state():
    b.update_status(request.args.get('state'))
    post_to_fb.main("the Nightbus is " + b.current_status + "!")

@app.route('/rider', methods=['GET'])
def home():
    status = b.get_current_status()
    return render_template("rider.html", status=status)

# I added this because the logged_in wasn't set to false everytime the application run which was breaking things.


@app.before_first_request
def intialize():
    session['logged_in'] = False
    db = database.get_session()
    if db.query(schema.Schedule).filter_by(id=1).first():
        db.close()
    else:
        session['logged_in'] = False
        monday = schema.Schedule(day="Monday")
        tuesday = schema.Schedule(day="Tuesday")
        wednesday = schema.Schedule(day="Wednesday")
        thursday = schema.Schedule(day="Thursday")
        friday = schema.Schedule(day="Friday")
        saturday = schema.Schedule(day="Saturday")
        sunday = schema.Schedule(day="Sunday")
        db.add(monday)
        db.add(tuesday)
        db.add(wednesday)
        db.add(thursday)
        db.add(friday)
        db.add(saturday)
        db.add(sunday)
        db.commit()
        db.close()



# normal app routes

@app.route('/')
def index():
    status = b.get_current_status()
    return render_template('index.html', status=status)

@app.route('/driver')
@login_required('driver')
def driver():
    return render_template('driver.html')


@app.route('/display')
def display():
    db = database.get_session()
    drivers = db.query(schema.Schedule).order_by(schema.Schedule.id).limit(7).all()
    return render_template('display.html', drivers = drivers)



@app.route('/schedule')
def schedule():
    db = database.get_session()
    drivers = db.query(schema.User).all()
    return render_template('schedule.html', drivers = drivers)


@app.route('/assignmonday',  methods=['POST'])
def assignmon():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=1).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))

@app.route('/assigntuesday',  methods=['POST'])
def assigntues():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=2).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))

@app.route('/assignwednesday',  methods=['POST'])
def assignwed():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=3).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))

@app.route('/assignthursday',  methods=['POST'])
def assignthurs():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=4).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))

@app.route('/assignfriday',  methods=['POST'])
def assignfri():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=5).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))

@app.route('/assignsaturday',  methods=['POST'])
def assignsat():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=6).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))

@app.route('/assignsunday',  methods=['POST'])
def assignsun():
    db = database.get_session()
    driver_id = request.form['driver_id']
    new = db.query(schema.User).filter_by(id=driver_id).first()
    day = db.query(schema.Schedule).filter_by(id=7).first()
    day.driver_id = new.id
    day.firstname = new.firstname
    day.lastname = new.lastname
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))


@app.route('/admin')
@login_required('admin')
def admin():
    return render_template('admin.html')

@app.route('/adduser')
@login_required('admin')
def adduser():
    return render_template('add.html')

@app.route('/add', methods=['POST'])
def add():

    db = database.get_session()

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
    new_driver = schema.User(firstname=firstname, lastname=lastname, username=username, email=email, role=role)


    # Add the new driver we defined above to the database using the built in method 'add' and once again using the built in method 'commit' make sure the record is permanently
    # entered into the databse.
    db.add(new_driver)
    db.commit()
    db.close()

    # Let's not forget to do a db.close() for all our sessions with the database. It won't make a difference right now but once we deploy the app or start testing it on Heroku
    # it will be a mess.

    # To check if a user has been successfully added to the database open a new tab in terminal, use the command psql nightbus to go to the nightbus database and do
    # SELECT * FROM "Users"; and it should be the last entry in that table.
    # Most of the stuff related to the databases I found at https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/ and http-demo

    flash("User successfully added")
    return redirect(url_for('admin'))

@app.route('/removeuser')
@login_required('admin')
def removeuser():
    return render_template('remove.html')

@app.route('/remove', methods=['POST'])
def remove():
    db = database.get_session()
    # This function is basically identical to the user addition function. We use the get_session method to create a connection with the database. Next we get the value of the username
    # that was entered in the form using the request library that comes with flask.
    username = request.form['username']

    # Next we use the query method to search the table User and we filter our query by the username we got above. This displays the first entry it gets so I don't know how we would handle
    # two different people having two different user names. More documentation on querying and just general sqlalchemy knowledge can be found at http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying
    # After that we just use the built in delete method to remove the user and then we have to make sure we commit after that to make the deletion permanent.
    user = db.query(schema.User).filter_by(username=username).first()
    user_auth = db.query(schema.Auth).filter_by(username=username).first()
    db.delete(user)
    #db.delete(user_auth)
    db.commit()
    db.close()


    flash('User successfully removed')
    return redirect(url_for('admin'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/username_exists', methods=['POST'])
def username_exists():
    db = database.get_session()
    username_exists = db.query(schema.User).filter_by(username=request.form['username']).first()
    if username_exists:
        return jsonify("Username is already taken. Please pick another.")
    else:
        return jsonify("true")

@app.route('/register', methods=['GET','POST'])
def register():

    db = database.get_session()
    # this function should allow anyone to register and be able to log in right now. Once we have that we can work on different views for different types of users and stuff like that.
    # it works in similar fashion like the add driver and remove driver functions it connects to the databases using the get session function and gets the data from the form using the
    # flask request module then it creates a User and an Auth entry. The user entry is just for keeping track of users while the auth entry will contain the username and the password
    # the person signed up with. We don't actually store the password we encrypt it using the passlib library that we imported above. We then add both entries to their respective
    # tables and we commit and then we are done.

    db = database.get_session()

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    role = (request.form['role']).lower()

    user = schema.User(firstname = firstname, lastname = lastname, email = email, username = username, role=role)
    user_auth = schema.Auth(username=username)
    user_auth.encrypt_password(password)

    db.add(user)
    db.add(user_auth)
    db.commit()


    # The next few lines automatically send an email to the email address the user entered when registering asking them to confirm their email. We use the generate_confirmation_token
    # we defined in our email_confimation module to generate a random token. The url they will get will be of the format localhost/confirm_email + token and when they click it they
    # should be redirected to the function immediately below.

#        subject = 'Confirm Your Email'
#        token = generate_confirmation_token(email, serializer)
#        confirm_url = url_for('confirm_email', token = token, _external=True)
#        html = render_template('activate.html', confirm_url = confirm_url)
#        send_mail(user.email, subject, html, mail)

    db.close()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/confirm/<token>')
def confirm_email(token):
    db = database.get_session()
    email = confirm_email_token(token, serializer)

    user = db.query(schema.User).filter_by(email=email).first()

    user_auth = db.query(schema.Auth).filter_by(username=user.username).first()
#    user_auth.confirmed = True

    db.add(user_auth)
    db.commit()
    db.close()

    flash('Email successfully confimed')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    db = database.get_session()
    username = request.form['username']
    password = request.form['password']

    user_auth = db.query(schema.Auth).filter_by(username=username).first()
    user = db.query(schema.User).filter_by(username=username).first()


    if user_auth:
        if user_auth.verify_password(password):
        #if user_auth.confirmed:
            session['username'] = username
            session['logged_in'] = True

            flash('Welcome')
            if str(user.role).lower() == 'admin':
                return redirect(url_for('admin'))
            elif str(user.role).lower() == 'driver':
                return redirect(url_for('driver'))
            else:
                return redirect(url_for('rider'))
        #else:
            #flash('Please confirm the email address associated with your account.')
            #return redirect(url_for('login'))

        else:
            flash('Invalid Credentials')
            return redirect(url_for('login'))
    else:
        return render_template('no_user.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect (url_for('home'))

@app.route('/no_user')
def no_user():
    return render_template('no_user.html')

##### Error Handling #####

# These four felt like the major and most commonly occuring errors and I only added error handling for them but if we need
# more error handling functionality we can just add the three lines here and add the corresponding html document in our
# templates folder. Error handlers are just functions that come with flask. More documentation can be found at
# http://flask.pocoo.org/docs/0.12/patterns/errorpages/


@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbiddenaccess(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def servererror(e):
    return render_template('500.html'), 500

@app.errorhandler(405)
def methodnotallowed(e):
    return render_template('405.html'), 405
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
