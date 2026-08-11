import os
from flask import Flask, render_template, request
from flask_livereload import LiveReload
from database.db_handler import dbHandler
from dotenv import load_dotenv

load_dotenv() # To load env secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Do not use this in production
livereload = LiveReload(app)

databaseHandler = dbHandler()

@app.route("/")
def landingPage():
    return render_template('index.html')

@app.route("/login", methods = ["GET", "POST"])
def account_page():
    if request.method == "POST":
        form_type = request.form.get('form_type')
        if form_type == 'signup_form':
            signup_name = request.form.get('signup_name')
            signup_username = request.form.get('signup_username')
            signup_email = request.form.get('signup_email')
            signup_password = request.form.get('signup_password')

            print('Signup name:', signup_name)
            print('Signup username:', signup_username)
            print('Signup email:', signup_email)
            print('Signup password', signup_password)

            databaseHandler.userRegistration(signup_name, signup_username, signup_email, signup_password)

        elif form_type == 'login_form':
            login_email = request.form.get('login_email')
            login_password = request.form.get('login_password')

            print('Login email:', login_email)
            print('Login password:', login_password)
    return render_template('login.html')
