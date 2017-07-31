import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, request
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
mail = Mail(app)

# I created a class that has all the configurations we need for the app to run. If we want to change the configuration or when we have to finally deploy the app
# we can just create another class called ProdConfig with the appropriate attributes. This wasn't necessary at this point but the main.py was getting messy.
app.config.from_object('config.TestConfig')
mail.init_app(app)

# We need to generate a unique token everytime a user registers to confirm their email. We use the URLSafeTimedSerializer serializer from the it's dangerous module.
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# functions for udating the NightBus's status and for updating the duration of the trip

status = "here"

def get_user(username):
    db = database.get_session()
    user = db.query(schema.User).filter_by(username=username).first()
    return user

class NightBus:
    def __init__(self):
        self.current_status = status
        self.trip_duration = 0
        self.origin = 'Reed College'
        self.destinations = []

        self.num_of_destinations = 0
    def get_current_status(self):
        return self.current_status
    def get_trip_duration(self):
        return self.trip_duration
    def update_status(self,new_status):
        self.current_status = new_status
    def update_origin(self, new_origin):
        self.origin = new_origin
    def get_origin(self):
        return self.origin
    def update_trip_duration(self, new_duration):
        self.trip_duration = new_duration
    def get_num_of_destinations(self):
        return self.num_of_destinations
    def update_num_of_destinations(self, new_num):
        self.num_of_destinations = new_num
    def get_destinations(self):
        return self.destinations
    def update_destinations(self, new_destinations):
        self.destinations = new_destinations


b  = NightBus()


#updates the status of the NightBus

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

@app.before_first_request
def intialize():
    #creates the database for the driver schedule. the if statement checks to see if the database already exists and passes if it does, otherwise it creates the database.
    db = database.get_session()
    username = request.environ.get('REMOTE_USER')
    
    if db.query(schema.Schedule).filter_by(id=1).first():
        if db.query(schema.Auth).filter_by(id=1).first():
                db.close()
        else:
                admin = schema.Auth(username="admin")
                admin.encrypt_password('123')
                db.add(admin)
                db.commit()
    else:
        admin = schema.Auth(username="admin")
        user_auth.encrypt_password('123')
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
    user = get_user(username)

    return render_template('rider.html', status=status, user=user)

@app.route('/driver')
def driver():
    #this accesses the driver schedule database and pulls out the drivers so a schedule can be created on the driver page

    db = database.get_session()
    drivers = db.query(schema.Schedule).order_by(schema.Schedule.id).limit(7).all()

    user = get_user(username)


    db.close()
    return render_template('driver.html', drivers=drivers, user=user)


@app.route('/schedule')
def schedule():

    #pulls out all the drivers from the User database so admins can assign them to shifts

    db = database.get_session()
    drivers = db.query(schema.User).all()
    db.close()
    return render_template('schedule.html', drivers = drivers)

@app.route('/login', methods = ['GET'])
def login():
    status = b.get_current_status()
    duration = b.get_trip_duration()
    return render_template("rider.html", status=status, duration=duration)



@app.route('/display')
def display():

    #displays the new driver schedule after the admin changes the schedule

    db = database.get_session()
    drivers = db.query(schema.Schedule).order_by(schema.Schedule.id).limit(7).all()
    db.close()
    return render_template('display.html', drivers = drivers)


@app.route('/assign', methods=['POST'])
def assign():

    #assigns the new driver to the driver schedule by running an if statment that checks if each day was passed a null value of "no", if it was
    #then it means that a new driver was not assigned so it passes. if it is not null then it opens up the database and goes to the corresponding day
    #and adds that driver as the driver for that day
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
    flash("Shift successfully assigned")
    return redirect(url_for('display'))


@app.route('/admin')
@login_required('admin')
def admin():
    user = get_user(username)

    return render_template('admin.html', user=user)

@app.route('/adduser')
@login_required('admin')
def adduser():
    return render_template('add.html')

@app.route('/add', methods=['POST'])
def add():


    db = database.get_session()

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
    return redirect(url_for('admin'))

@app.route('/removeuser')
@login_required('admin')
def removeuser():
    db = database.get_session()
    drivers = db.query(schema.User).all()
    db.close()
    return render_template('remove.html', drivers = drivers)

@app.route('/remove', methods=['POST'])
def remove():
    db = database.get_session()

    username = request.form['username']

    user = db.query(schema.User).filter_by(username=username).first()
    user_auth = db.query(schema.Auth).filter_by(username=username).first()
    if user:
        db.delete(user)
        if user_auth:
            db.delete(user_auth)
        else:
            pass
        db.commit()
        db.close()
        return redirect(url_for('removeuser'))

    else:
        return redirect(url_for('no_user'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect (url_for('home'))

@app.route('/no_user')
def no_user():
    return render_template('no_user.html')

@app.route('/drivermaps')
@login_required('driver')
def drivermaps():
    origin = b.get_origin()
    destinations = b.get_destinations()
    num_of_destinations = int(b.get_num_of_destinations())
    no_destination = False
    return render_template('maps.html', origin = origin,  destinations = destinations, no_destination = no_destination, num_of_destinations=num_of_destinations)



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

