from flask import Flask, render_template
app = Flask(__name__)

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

@app.route('/remove')
def rmDriver():
    return render_template('remove.html')

if __name__ == '__main__':
        app.run()
