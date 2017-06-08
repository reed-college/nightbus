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
                if str(user.role).lower() == 'admin' or str(user.role).lower() == str(role).lower():
                    return function(*args, **kwargs)
                else:
                    return render_template('no_access.html')

            else:
                flash("Invalid Credentials")
                return redirect(url_for('login'))
        return wrap
    return wrapper
