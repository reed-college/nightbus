from flask import Flask, render_template, request, session, redirect, url_for, flash
from decorators import login_required
import schema
import database
import post_to_fb

#from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)
app.secret_key = 'This is secret'
#auth = HTTPBasicAuth()
db = database.get_session()


#ajax and global status

status = "here"

class NightBus:
    def __init__(self):
        self.current_status = status
    def get_current_status(self):
        return self.current_status
    def update_status(self,new_status):
        self.current_status = new_status


b  = NightBus()


# I added this because the logged_in wasn't set to false everytime the application run which was breaking things.
#@app.before_request
#def set_session():
  #  session['logged_in'] = False

@app.route('/update_state/')
def update_state():
    b.update_status(request.args.get('state'))
    post_to_fb.main("the Nightbus is " + b.current_status + "!")

@app.route('/rider', methods=['GET'])
def display_status():
    status = b.get_current_status()
    return render_template("rider.html", status=status)

# normal app routes

@app.route('/', methods=['GET'])
def home():
    status = b.get_current_status()
    return render_template('index.html', status=status)

@app.route('/driver')
# @login_required('driver')
def driver():
    return render_template('driver.html')




##### begin test ######

@app.route('/schedule')
# @login_required('driver')
def schedule():
    drivers = db.query(schema.User).all()
    return render_template('schedule.html', drivers = drivers)


@app.route('/assignmonday',  methods=['POST'])
def assign():
    driver_id = request.form['driver_id']
    #old = db.query(schema.Monday).first()
    #db.delete(old)
    #db.commit()
    new = db.query(schema.User).filter_by(id=driver_id).first()
    db.query(schema.Monday).add(new)
    db.commit()
    flash("Shift successfully assigned")
    return redirect(url_for('schedule'))



##### end test #######

@app.route('/admin')
# @login_required('admin')
def admin():
    return render_template('admin.html')

@app.route('/add')
@login_required('admin')
def addDriver():
    return render_template('add.html')



@app.route('/adduser', methods=['POST'])
def addUser():

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

    # To check if a user has been successfully added to the database open a new tab in terminal, use the command psql nightbus to go to the nightbus database and do
    # SELECT * FROM "Users"; and it should be the last entry in that table.
    # Most of the stuff related to the databases I found at https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/ and http-demo

    flash("User successfully added")
    return redirect(url_for('admin'))

@app.route('/remove')
@login_required('admin')
def rmDriver():
    return render_template('remove.html')

@app.route('/removeuser', methods=['POST'])
def removeUser():
    # This function is basically identical to the user addition function. We use the get_session method to create a connection with the database. Next we get the value of the username
    # that was entered in the form using the request library that comes with flask.
    username = request.form['username']

    # Next we use the query method to search the table User and we filter our query by the username we got above. This displays the first entry it gets so I don't know how we would handle
    # two different people having two different user names. More documentation on querying and just general sqlalchemy knowledge can be found at http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying
    # After that we just use the built in delete method to remove the user and then we have to make sure we commit after that to make the deletion permanent.
    user = db.query(schema.User).filter_by(username=username).first()
    user_auth = db.query(schema.Auth).filter_by(username=username).first()
    db.delete(user)
    db.delete(user_auth)
    db.commit()


    flash('User successfully removed')
    return redirect(url_for('admin'))

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

    return "User successfully registered"

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    user_auth = db.query(schema.Auth).filter_by(username=username).first()
    user_role = db.query(schema.User).filter_by(username=username).first()

    if user_auth:
        if user_auth.verify_password(password):
            session['username'] = username
            session['logged_in'] = True

            return redirect(url_for('home'))

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

if __name__ == '__main__':
    app.run()
