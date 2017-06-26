# This python view decorator is what we use to make certain routes require login and certain previlages. 
# The way this is supposed to work is it checkes if a user is logged in or not if the user is not logged
# in it asks the user to log in. Once the user logs in they will have entered their username so we then
# use that username to query our User database and check if the user exists if the username doesn't exist
# it tells them to sign up. The signup page then should redirect them to the log in page and the whole
# process begins again. This time if the username exists in our database we check to see what kind of 
# role the user has. If they have an admin role they have access to all pages in the site. If they have
# a driver role they have access to the driver and rider page and if they are a rider they only have access
# to the rider page. 

# We used decorators because that is what most sites recommended we do and it made things really easier.
# One thing that came up during our research on implementing a user auth system for flask is the availability
# of libraries and modules that can handle it for us but since we tried to keep the number of external
# modules we use to a minimum we decided to write our own decorator. 

# A documentation on flask view decorators can be found at http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from flask import session, flash, redirect, url_for, render_template
from functools import wraps
import schema
import database


db = database.get_session()

def login_required(role):
    def wrapper(function):
        @wraps(function)
        def wrap(*args, **kwargs):
            if session['logged_in']:
                username = session['username']
                user = db.query(schema.User).filter_by(username=username).first()
                if user:
                    if str(user.role).lower() == str(role).lower() or str(user.role).lower() == 'admin':
                        return function(*args, **kwargs)
                    else:
                        return render_template('no_access.html')
                else:
                    return render_template('no_user.html')

            else:
                if str(role).lower() == 'driver':
                    return redirect(url_for('driverlogin'))
                elif str(role).lower() == 'admin':
                    return redirect(url_for('adminlogin'))
                else:
                    return render_template('500.html')
        return wrap
    return wrapper
