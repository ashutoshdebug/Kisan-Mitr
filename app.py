import os
import requests
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_livereload import LiveReload
from database.db_handler import dbHandler
from engine.dataAcquisition import dataAcquision
from utils.filenFolderPath import fileFolderPath
from dotenv import load_dotenv
from engine.vision_model import visionModel

load_dotenv() # To load env secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Do not use this in production
livereload = LiveReload(app)

databaseHandler = dbHandler()
folderHandler = fileFolderPath()
visionModel = visionModel()
dataAcquire = dataAcquision()

@app.route("/")
def landingPage():
    if databaseHandler.login_successful:
        msg = f"Hi {databaseHandler.username}!"
        return render_template('index.html', user_var = msg, account_or_upload = "upload")
    return render_template('index.html', account_or_upload = "account_page")


@app.route("/logout", methods = ["GET", "POST"])
def logout():
    data = request.get_json()
    # print(data)
    logout = data.get("logout")

    # print("Logout value:", logout)

    if logout == True:
        databaseHandler.login_successful = False

    response = {
        "status": "success"
    }
    return jsonify(response), 200


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('pageNotFound.html'), 404


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

    if not visionModel.result_generated:
        return redirect(url_for('upload'))

    return render_template('result.html')


@app.route("/acquire", methods=["GET", "POST"])
def acquire():

    if not databaseHandler.login_successful:
        return redirect(url_for('account_page'))

    session["username"] = databaseHandler.username
    session["user-image"] = databaseHandler.imagePath

    if session["username"] is None or session["user-image"] is None:
        return redirect(url_for('upload'))

    user = session["username"]
    user_image = session["user-image"]

    static_path = os.path.join(app.root_path, "static")
    user_image = os.path.relpath(
        user_image,
        static_path
    ).replace("\\", "/")

    print("User image path:", user_image)

    if request.method == "POST":

        location = request.form.get('location')
        crop_season = request.form.get('season')
        temperature = request.form.get('temperature')
        humidity = request.form.get('humidity')
        rainfall = request.form.get('rainfall')
        windspeed = request.form.get('windspeed')
        variety = request.form.get('variety')
        irrigation = request.form.get('irrigation')
        soil = request.form.get('soil')
        symptoms = request.form.get('symptoms')

        prompt = dataAcquire.allFields(location, crop_season, temperature, humidity, rainfall, windspeed, variety, irrigation, soil, symptoms)

        image_path = databaseHandler.getImagePath(databaseHandler.username)

        # print("Image path in app:", image_path)

        result = visionModel.engine(image_path, prompt)

        print("AI Result:")
        print(result)

        
        if result is None:
            return render_template('acquireInfo.html', user=user, user_image=user_image, error="Unable to generate a valid diagnosis.")

        return render_template('result.html', user=user, user_image=user_image, result=result)

    return render_template('acquireInfo.html', user=user, user_image=user_image)


# @app.route('/getCurrentPosition', methods=["POST"])
# def get_current_position():
#     data = request.get_json()

#     latitude = data.get("latitude")
#     longitude = data.get("longitude")

#     print("Latitude:", latitude)
#     print("Longitude:", longitude)

#     response = requests.get(
#         "https://nominatim.openstreetmap.org/reverse",
#         params={
#             "lat": latitude,
#             "lon": longitude,
#             "format": "json"
#         },
#         headers={
#             "User-Agent": "MyFlaskApp/1.0"
#         }
#     )

#     location_data = response.json()

#     print("Location:", location_data.get("display_name"))

#     return {
#         "latitude": latitude,
#         "longitude": longitude
#     }


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
            databaseHandler.getImagePath(databaseHandler.username)
            return redirect(url_for('acquire'))
            
    return render_template('upload.html', account_or_upload = "account_page")

