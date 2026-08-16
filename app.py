import os
import requests
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
from flask_livereload import LiveReload
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath
from dotenv import load_dotenv
# Temporary
from engine.vision_model import visionModel
import time
# -------------------------------------------

load_dotenv() # To load env secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Do not use this in production
livereload = LiveReload(app)

databaseHandler = dbHandler()
folderHandler = fileFolderPath()
visionModel = visionModel()

@app.route("/")
def landingPage():
    return render_template('index.html')



@app.route("/motive")
def motivePage():
    return render_template("motive.html")



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
            return redirect(url_for('account_page'))

        elif form_type == 'login_form':
            login_email = request.form.get('login_email')
            login_password = request.form.get('login_password')

            print('Login email:', login_email)
            print('Login password:', login_password)

            databaseHandler.verifyUser(login_password, login_email)

            if databaseHandler.login_successful:
                folderHandler.createFolder(databaseHandler.username)
                return redirect(url_for('upload'))

    return render_template('login.html')



@app.route("/result")
def results():
    if not databaseHandler.login_successful:
        return redirect(url_for('account_page'))

    return render_template('result.html')


@app.route("/acquire")
def acquire():
    if not databaseHandler.login_successful:
        return redirect(url_for('account_page'))

    return render_template('acquireInfo.html')



@app.route('/getCurrentPosition', methods=["POST"])
def get_current_position():
    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    response = requests.get(
        "https://nominatim.openstreetmap.org/reverse",
        params={
            "lat": latitude,
            "lon": longitude,
            "format": "json"
        },
        headers={
            "User-Agent": "MyFlaskApp/1.0"
        }
    )

    location_data = response.json()

    print("Location:", location_data.get("display_name"))

    return {
        "latitude": latitude,
        "longitude": longitude
    }


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not databaseHandler.login_successful:
        return redirect(url_for('account_page'))

    if request.method == "POST":
        file = request.files['fileInput']

        if file.filename == "":
            print("No selected file")
            return redirect(request.url)

        if file:
            folderHandler.filSave(file)
            # print("File path committed")
            databaseHandler.addImageName(databaseHandler.username, folderHandler.new_name)

            # Result processing and AI enabler
            # databaseHandler.getImagePath(databaseHandler.username)
            image_path = databaseHandler.getImagePath(databaseHandler.username)
            # print("Image path in app:", image_path)
            # time.sleep(1.5)
            # print(visionModel.engine(image_path))
            
    return render_template('upload.html')

