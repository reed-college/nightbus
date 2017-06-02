from flask import session, flash, redirect, url_for
from functools import wraps
import schema
import database


db = database.get_session()

def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if session['logged_in']:
            return function(*args, **kwargs)
        else:
            flash('You need to log in first')
            return redirect(url_for('login'))
    return wrap

def user_is(role):
    def wrapper(function):
        @wraps(function)
        def wrap(*args, **kwargs):
            username = session['username']
            user = db.query(schema.User).filter_by(username=username).first()
            if user.role == role:
                return function(*args, **kwargs)
            else:
                flash("You don't have permissions to view this page")
                return redirect(url_for('login'))
        return wrap
    return wrapper


