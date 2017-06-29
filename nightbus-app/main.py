import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from decorators import login_required
from flask_mail import Message, Mail
from user_handling import generate_confirmation_token, confirm_email_token, send_mail
from itsdangerous import URLSafeTimedSerializer
from tracking import calculate_duration
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
        self.trip_duration = 0
        self.origin = None
        self.destinations = []
    def get_current_status(self):
        return self.current_status
    def get_trip_duration(self):
        return self.trip_duration
    def update_status(self,new_status):
        self.current_status = new_status
    def update_trip_duration(self, new_duration):
        self.trip_duration = new_duration
    def get_destinations(self):
        return self.destinations
    def update_destinations(self, new_destinations):
        self.destinations = new_destinations
    def get_origin(self):
        return self.origin
    def update_origin(self, new_origin):
        self.origin = new_origin


b  = NightBus()

@app.route('/update_state/')
def update_state():
    b.update_status(request.args.get('state'))
    post_to_fb.main("the Nightbus is " + b.current_status + "!")
    return ('', 204)

@app.route('/rider', methods=['GET'])
def home():
    status = b.get_current_status()
    duration = b.get_trip_duration()
    return render_template("rider.html", status=status, duration=duration)


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
    duration = b.get_trip_duration()
    return render_template('rider.html', status=status, duration=duration)

@app.route('/driver')
@login_required('driver')
def driver():
    db = database.get_session()
    drivers = db.query(schema.Schedule).order_by(schema.Schedule.id).limit(7).all()
    db.close()
    return render_template('driver.html', drivers=drivers)


@app.route('/schedule')
def schedule():
    db = database.get_session()
    drivers = db.query(schema.User).all()
    db.close()
    return render_template('schedule.html', drivers = drivers)


@app.route('/display')
def display():
    db = database.get_session()
    drivers = db.query(schema.Schedule).order_by(schema.Schedule.id).limit(7).all()
    db.close()
    return render_template('display.html', drivers = drivers)


@app.route('/assign', methods=['POST'])
def assign():
    drivers= request.form.getlist('drivers[]')

    db = database.get_session()

    if drivers[0] == "No":
        pass
    else:
        mon = db.query(schema.Schedule).filter_by(day='Monday').first()
        monDriver = db.query(schema.User).filter_by(id=drivers[0]).first()
        mon.driver_id = monDriver.id
        mon.firstname = monDriver.firstname
        mon.lastname = monDriver.lastname

    if drivers[1] == "No":
        pass
    else:
        tue = db.query(schema.Schedule).filter_by(day='Tuesday').first()
        tueDriver = db.query(schema.User).filter_by(id=drivers[1]).first()
        tue.driver_id = tueDriver.id
        tue.firstname = tueDriver.firstname
        tue.lastname = tueDriver.lastname

    if drivers[2] == "No":
        pass
    else:
        wed = db.query(schema.Schedule).filter_by(day='Wednesday').first()
        wedDriver = db.query(schema.User).filter_by(id=drivers[2]).first()
        wed.driver_id = wedDriver.id
        wed.firstname = wedDriver.firstname
        wed.lastname = wedDriver.lastname

    if drivers[3] == "No":
        pass
    else:
        thu = db.query(schema.Schedule).filter_by(day='Thursday').first()
        thuDriver = db.query(schema.User).filter_by(id=drivers[3]).first()
        thu.driver_id = thuDriver.id
        thu.firstname = thuDriver.firstname
        thu.lastname = thuDriver.lastname

    if drivers[4] == "No":
        pass
    else:
        fri = db.query(schema.Schedule).filter_by(day='Friday').first()
        friDriver = db.query(schema.User).filter_by(id=drivers[4]).first()
        fri.driver_id = friDriver.id
        fri.firstname = friDriver.firstname
        fri.lastname = friDriver.lastname

    if drivers[5] == "No":
        pass
    else:
        sat = db.query(schema.Schedule).filter_by(day='Saturday').first()
        satDriver = db.query(schema.User).filter_by(id=drivers[5]).first()
        sat.driver_id = satDriver.id
        sat.firstname = satDriver.firstname
        sat.lastname =  satDriver.lastname

    if drivers[6] == "No":
        pass
    else:
        sun = db.query(schema.Schedule).filter_by(day='Sunday').first()
        sunDriver = db.query(schema.User).filter_by(id=drivers[6]).first()
        sun.driver_id = sunDriver.id
        sun.firstname = sunDriver.firstname
        sun.lastname =  sunDriver.lastname

    db.commit()
    db.close()

    # flash("Shift successfully assigned")
    return redirect(url_for('display'))


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
    
    subject = 'Set Your Password'
    token = generate_confirmation_token(email, serializer)
    set_password_url = url_for('set_password', token = token, _external=True)
    html = render_template('activate.html', set_password_url = set_password_url)
    send_mail(email, subject, html, mail)


    # To check if a user has been successfully added to the database open a new tab in terminal, use the command psql nightbus to go to the nightbus database and do
    # SELECT * FROM "Users"; and it should be the last entry in that table.
    # Most of the stuff related to the databases I found at https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/ and http-demo

    return redirect(url_for('admin'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":

        email = request.form['email']

        subject = 'Reset Your Password'
        token = generate_confirmation_token(email, serializer)
        reset_password_url = url_for('reset_password', token=token, _external=True)
        html = render_template('reset.html', reset_password_url = reset_password_url)
        send_mail(email, subject, html, mail)

        return render_template('check_email.html')

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == "POST":
        db = database.get_session()
        email = confirm_email_token(token, serializer)

        user = db.query(schema.User).filter_by(email=email).first()
        
        new_password = request.form['password']

        user_auth = db.query(schema.Auth).filter_by(username=user.username).first()
        user_auth.encrypt_password(new_password)

        db.add(user_auth)
        db.commit()

        if user.role == 'admin':
            db.close()
            return redirect(url_for('adminlogin'))
        else:
            db.close()
            return redirect(url_for('adminlogin'))
    else:
        return render_template('reset_password.html', token = token)


@app.route('/set_password/<token>', methods=['GET', 'POST'])
def set_password(token):
    if request.method == "POST":
        db = database.get_session()
        email = confirm_email_token(token, serializer)

        user = db.query(schema.User).filter_by(email=email).first()
        
        new_password = request.form['password']

        user_auth = schema.Auth(username=user.username)
        user_auth.encrypt_password(new_password)


        db.add(user_auth)
        db.commit()
        
        if user.role == 'admin':
            db.close()
            return redirect(url_for('adminlogin'))
        else:
            db.close()
            return redirect(url_for('driverlogin'))
    return render_template('confirm_password.html', token = token)
    



@app.route('/removeuser')
@login_required('admin')
def removeuser():
    if session['logged_in']:
        return render_template('remove.html')
    else:
        return redirect(url_for('adminlogin'))

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
    if user:
        db.delete(user)
        db.delete(user_auth)
        db.commit()
        db.close()

        return redirect(url_for('admin'))

    else:
        return redirect(url_for('no_user'))


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

@app.route('/email_exists', methods=['POST'])
def email_exists():
    db = database.get_session()
    email_exists = db.query(schema.User).filter_by(email=request.form['email']).first()
    if email_exists:
        return jsonify("Email address is already registered. Please login instead.")
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
    if user.role == 'admin':
        return redirect(url_for('adminlogin'))
    else:
        return redirect(url_for('driverlogin'))

@app.route('/confirm/<token>')
def confirm_email(token):
    db = database.get_session()
    email = confirm_email_token(token, serializer)

    user = db.query(schema.User).filter_by(email=email).first()

    user_auth = db.query(schema.Auth).filter_by(username=user.username).first()

    db.add(user_auth)
    db.commit()
    db.close()

    flash('Email successfully confimed')
    return redirect(url_for('login'))

@app.route('/driverlogin', methods=['GET', 'POST'])
def driverlogin():
    if request.method == 'POST':
        db = database.get_session()
        username = request.form['username']
        password = request.form['password']

        user_auth = db.query(schema.Auth).filter_by(username=username).first()
        user = db.query(schema.User).filter_by(username=username).first()

        if user_auth:
            if user_auth.verify_password(password):
                session['username'] = username
                session['logged_in'] = True

                return redirect(url_for('driver'))
            else:
                return redirect(url_for('driverlogin'))
        else:
            return render_template('no_user.html')
    else:
        return render_template('driver_login.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        db = database.get_session()
        username = request.form['username']
        password = request.form['password']

        user_auth = db.query(schema.Auth).filter_by(username=username).first()
        user = db.query(schema.User).filter_by(username=username).first()

        if user_auth:
            if user_auth.verify_password(password):
                session['username'] = username
                session['logged_in'] = True
                session['role'] = str(user.role).lower()

                return redirect(url_for('admin'))
            else:
                return redirect(url_for('admin_login.html'))
        else:
            return render_template('no_user.html')
    else:
        return render_template('admin_login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect (url_for('home'))

@app.route('/no_user')
def no_user():
    return render_template('no_user.html')

@app.route('/tracking', methods=['GET', 'POST'])
@login_required('driver')
def tracking():
    if request.method == 'POST':
        num_destinations = request.form['num_destinations']
        origin = request.form['origin']

        destinations = [None] * int(num_destinations)

        for i in range(int(num_destinations)):
            destinations[i] = request.form['address' + str(i+1)]

        destinations.append(origin)

        duration = 0
        for destination in destinations:
            duration += calculate_duration(origin, [destination])
            origin = destination
    
        print(duration)


        b.update_trip_duration(duration)
        b.update_destinations(destinations)
        b.update_origin(origin)

        return redirect(url_for('drivermaps'))

    return render_template('tracking.html')

@app.route('/drivermaps')
@login_required('driver')
def drivermaps():
    origin = b.get_origin()
    destinations = b.get_destinations()
    no_destination = False

    return render_template('maps.html', origin = origin,  destinations = destinations, no_destination = no_destination)
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
