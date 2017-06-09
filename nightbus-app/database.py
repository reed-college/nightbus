# We need the os module so that we can set the database url using environment variables as opposed to hard coding it into our code.
# The sessionmaker is used to create a connection with our database and more documentation on that can be found at 
# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#what-does-the-session-do
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker


url = "postgres://postgres@localhost/nightbus"

# The engine is the starting point for any application that uses databases. It creates the appropirate dialect and pool to communicate
# with our database. If we use postgresql then it will use dialect appropriate for postgreql and if we decide to use sqlite it will
# use a dialect compatible with that.

# Try to create an engine with the given url and if it fails instead of going haywire and breaking everything print a line that says
# sqlalchemy couldn't connect to the database.
try:
    engine = sqlalchemy.create_engine(url)
except sqlalchemy.exc.OperationalError:
    print("Failed to connect to the database.")


# We are going to use the get_session function to create a connection to our database using sessions and it can be used just like any 
# other python function you just have to import it into your application. It returns a session object that uses our predefined engine.
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


