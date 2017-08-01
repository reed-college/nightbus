# ![nightbus](http://68.media.tumblr.com/33216ea5cde4feca05bbc3f2553e827d/tumblr_nx1ppi6ZZo1s4p4gno1_500.gif)

# Welcome to the Reed College Nightbus App GitHub!

The Reed College Nightbus App is a Flask-based web application designed to facilitate two aspects of the student run Nightbus organization. First, the app allows students to see the "status" of the Nightbus, including information regarding whether it is on Campus, has just left, or is returning. Second, the app allows the Nightbus coordinators to do various adminstrative tasks, including assigning drivers to a specific shift and cancelling the Nightbus for the night. 

# Local Development Setup

This is how you get ready to do development work on the Nightbus app:

1. Make a virtual environment in python 3.6. The best way to do this is to install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/ 'virtualenvwrapper') and use the `mkvirtualenv` command. The proper command looks like this: `mkvirtualenv nightbus -p python3`. 
2. Install postgres to manage the database. On a mac, you can do this with [postgres.app](https://postgresapp.com/ 'postgres.app'). You can download postgres for windows [here](https://www.postgresql.org/download/windows/ 'postgres for windows').
3. Set up a directory on your computer to house the files for the Nightbus app. We recommend calling this directory `nightbus`. Once you have set that up, clone this git repo into the directory with `git clone https://github.com/reed-college/nightbus.git`
4. Check to make sure that everything has gone smoothly up to this point! You should have a file structure that looks something like this:

```
nightbus
|- README.md
|- requirements.py
|- nightbus-app
    |- templates
    |- static
    |- ...
```

5. Activate your `nightbus` virtual environment with the `workon nightbus` command, and download all the packages neccesary to run the nightbus app from `requirements.txt`. 
6. Set up the database
7. Make sure you have the `local_config.py` set up and filled with the correct info.
8. While in the `nightbus` directory, you can run the app with `python nightbus-app`. Your terminal should display something like `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`.
9. In your browser, go to `http://127.0.0.1:5000/` and you should see the app running!

# Deploying the App

1. Email Jason Meinzer or another Reed CIS staff member in order to gain access to the Reed server. They will ask you to send them your ssh public key for the repo.
2. `ssh nightbus@sds.reed.edu` in your terminal in order to enter into the Reed virtualenv. If you are prompted for a password check wheter your password protected your ssh key, if so enter that password. If you did not password protect your ssh key then you do not yet have access to the server.
3. From there if you `ls` you can see that there is a nightbus folder that contains a similar repo as the development one. 
4. To make changes it is suggested that you edit files from your local host, upload them to github, and then `git pull` in the nightbus repo on the Reed server to commit those changes. Though you may switches branches on the Reed server, the NightBus uses the "reed" branch as its master while local host uses "master", so make sure you are updating the correct branch. The reason for this difference is to prevent the override of certain fies and lines that allow the app to run on the server. Finally, after making changes, to restart the server so that the commits can be integrated type `touch nightbus.wsgi` while in the nightbus directory. This file runs the app with the Reed Apache server and will update the timestamp on the app.
5. To see the changes go to nightbus.reed.edu.
6. Note: Be sure you do not override "nightbus.wsgi" from the server or else the app will not run. In the case that you do accidently do this, contact Jason Meinzer or CIS staff member.
