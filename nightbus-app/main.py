from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Home Page'

@app.route('/rider')
def rider():
    return 'Riders Page'

@app.route('/driver')
def driver():
    return 'Drivers Page'

@app.route('/admin')
def admin():
    return 'Admins Page'

@app.route('/add')
def addDriver():
    return 'Add Drivers Page'

@app.route('/remove')
def rmDriver():
    return 'Remove Drivers Page'

if __name__ == '__main__':
        app.run()
