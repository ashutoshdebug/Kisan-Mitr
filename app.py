import os
import requests
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from flask_livereload import LiveReload
from routes.landing import register_landing_page
from routes.logout import register_logout_page
from routes.pageNotFound import register_pageNotFound_page
from routes.motivePage import register_motivePage
from routes.login import register_login_page
from routes.profile import register_profile_page
from database.db_handler import dbHandler
from engine.dataAcquisition import dataAcquision
from utils.filenFolderPath import fileFolderPath
from dotenv import load_dotenv
from engine.vision_model import visionModel

load_dotenv()  # To load env secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Do not use this in production
livereload = LiveReload(app)

databaseHandler = dbHandler()
folderHandler = fileFolderPath()
visionModel = visionModel()
dataAcquire = dataAcquision()


register_landing_page(app)
register_logout_page(app)
register_pageNotFound_page(app)
register_motivePage(app)
register_login_page(app)
register_profile_page(app)


@app.route("/result")
def results():
    if "username" not in session:
        return redirect(url_for("account_page"))

    username = session["username"]
    # msg = f"Hi {databaseHandler.username}!"
    user_var = True
    profile_image = folderHandler.getPFPImage(app.root_path, username)
    profile_data = databaseHandler.getProfileData(username)

    if not visionModel.result_generated:
        return redirect(url_for("upload"))

    return render_template("result.html", account_or_upload="upload", profile_image=profile_image, user_var = user_var, profile_name = profile_data[0])


@app.route("/acquire", methods=["GET", "POST"])
def acquire():

    if "username" not in session:
        return redirect(url_for("account_page"))

    # msg = f"Hi {databaseHandler.username}!"
    user_var = True
    username = session["username"]
    profile_data = databaseHandler.getProfileData(username)
    profile_image = folderHandler.getPFPImage(app.root_path, username)


    # session["username"] = databaseHandler.username
    image_path = databaseHandler.getImagePath(username)
    session["user-image"] = databaseHandler.imagePath

    if session["username"] is None or session["user-image"] is None:
        return redirect(url_for("upload"))

    user = session["username"]
    user_image = session["user-image"]

    static_path = os.path.join(app.root_path, "static")
    user_image = os.path.relpath(user_image, static_path).replace("\\", "/")

    print("User image path:", user_image)

    if request.method == "POST":

        location = request.form.get("location")
        crop_season = request.form.get("season")
        temperature = request.form.get("temperature")
        humidity = request.form.get("humidity")
        rainfall = request.form.get("rainfall")
        windspeed = request.form.get("windspeed")
        variety = request.form.get("variety")
        irrigation = request.form.get("irrigation")
        soil = request.form.get("soil")
        symptoms = request.form.get("symptoms")

        prompt = dataAcquire.allFields(location, crop_season, temperature, humidity, rainfall, windspeed, variety, irrigation, soil, symptoms)

        databaseHandler.insertCropProperties(username, location, crop_season, temperature, humidity, rainfall, windspeed, variety, irrigation, soil, symptoms)

        image_path = databaseHandler.getImagePath(username)

        # print("Image path in app:", image_path)
        
        in_development = os.getenv("in_development") == "True"
        # print(type(in_development))
        # print(in_development)

        if in_development:
            with open("development_assets/result.json", "r", encoding="utf-8") as file:
                result = json.load(file)
            return render_template(
                        "result.html", user=user, user_image=user_image, result=result, user_var = user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload = "upload"
            )

        result = visionModel.engine(image_path, prompt)

        # print(result)
        # print("AI Result:")

        if result is None:
            return render_template("acquireInfo.html", user=user, user_image = user_image, user_var = user_var, profile_image=profile_image,profile_name = profile_data[0],error="Unable to generate a valid diagnosis.", account_or_upload="upload",)

        folderHandler.saveJsonFile(visionModel.result)
        databaseHandler.addResultName(username, folderHandler.result_file)
        databaseHandler.getResultFilePath(username)

        try:
            with open(databaseHandler.resultPath, "r", encoding="utf-8") as file:
                result = json.load(file)
                
        except (OSError, TypeError,  json.JSONDecodeError) as err:
            print("JSON open err:", err)
            return False

        return render_template(
            "result.html", user=user, user_image=user_image, result=result, user_var = user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload = "upload"
        )
        

    return render_template("acquireInfo.html", user=user, user_image=user_image, user_var = user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload="upload",)



@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("account_page"))

    username = session["username"]
    # if databaseHandler.login_successful:
    # msg = f"Hi {databaseHandler.username}!"
    user_var = True
    profile_data = databaseHandler.getProfileData(username)
    profile_image = folderHandler.getPFPImage(app.root_path, username)

    # return render_template("upload.html", user_var = msg, account_or_upload = "upload")

    if request.method == "POST":
        file = request.files["fileInput"]

        if file.filename == "":
            print("No selected file")
            return redirect(request.url)

        if file:
            folderHandler.fileSave(file)
            # print("File path committed")
            databaseHandler.addImageName(
                username, folderHandler.new_name
            )
            databaseHandler.getImagePath(username)
            return redirect(url_for("acquire"))

    return render_template("upload.html", user_var= user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload="upload")