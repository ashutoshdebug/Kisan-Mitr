import os
import requests
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from flask_livereload import LiveReload
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


@app.route("/")
def landingPage():
    if "username" in session:
        username = session["username"]
    # if databaseHandler.login_successful:
        user_var = True
        profile_data = databaseHandler.getProfileData(username)
        profile_image = folderHandler.getPFPImage(app.root_path, username)
        return render_template("index.html", user_var = user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload="upload")
    return render_template("index.html", account_or_upload="account_page")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    # data = request.get_json()
    # # print(data)
    # logout = data.get("logout")

    # # print("Logout value:", logout)

    # if logout == True:
    #     databaseHandler.login_successful = False
    session.clear()
    response = {"status": "success"}
    return jsonify(response), 200


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("pageNotFound.html"), 404


@app.route("/motive")
def motivePage():
    # if databaseHandler.login_successful:
    if "username" in session:
        username = session["username"]
        user_var = True
        profile_data = databaseHandler.getProfileData(username)
        profile_image = folderHandler.getPFPImage(app.root_path, username)
        return render_template("motive.html", profile_image=profile_image, user_var=user_var, profile_name = profile_data[0], account_or_upload="upload")
    return render_template("motive.html", account_or_upload="account_page")


@app.route("/login", methods=["GET", "POST"])
def account_page():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "signup_form":
            signup_name = request.form.get("signup_name")
            signup_username = request.form.get("signup_username")
            signup_email = request.form.get("signup_email")
            signup_password = request.form.get("signup_password")

            print("Signup name:", signup_name)
            print("Signup username:", signup_username)
            print("Signup email:", signup_email)
            print("Signup password", signup_password)

            databaseHandler.userRegistration(signup_name, signup_username, signup_email, signup_password)

            if databaseHandler.user_already_exist is True:
                return jsonify({"user_already_exist": True})
            
            return redirect(url_for("account_page"))

        elif form_type == "login_form":
            login_email = request.form.get("login_email")
            login_password = request.form.get("login_password")

            print("Login email:", login_email)
            print("Login password:", login_password)

            databaseHandler.verifyUser(login_password, login_email)

            if databaseHandler.user_not_exist is True:
                return jsonify({"not_exist": True}), 200

            if databaseHandler.login_successful:
                session.clear()
                session["username"] = databaseHandler.username
                folderHandler.createFolder(databaseHandler.username)
                return redirect(url_for("upload"))
            

    return render_template("login.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "username" not in session:
        return redirect(url_for("account_page"))

    username = session["username"]

    folderHandler.createFolder(username)

    if request.method == "POST":
        if request.is_json:
            data = request.get_json()

            if data.get("remove_image") is True:

                try:
                    for item in Path(folderHandler.pfp_custom).iterdir():
                        if item.is_file():
                            item.unlink()

                    return jsonify({
                        "status": "success"
                    }), 200

                except OSError as err:
                    print("Remove PFP error:", err)

                    return jsonify({
                        "status": "error"
                    }), 500

        profile_file = request.files.get("profile_image")

        if profile_file and profile_file.filename:

            success = folderHandler.addCustomPfP(profile_file)

            if not success:
                return jsonify({
                    "status": "error",
                    "message": "Unable to save profile image."
                }), 500

            return redirect(url_for("profile"))

    profile_data = databaseHandler.getProfileData(username)

    profile_image = folderHandler.getPFPImage(app.root_path, username)

    has_custom_profile_image = (
        folderHandler.getCustomPfP() is not None
    )

    return render_template(
        "profile.html",
        user_var=True,
        profile_name=profile_data[0],
        profile_image=profile_image,
        has_custom_profile_image=has_custom_profile_image,
        profile_name_user=profile_data[0],
        profile_email=profile_data[1],
        profile_username=profile_data[2]
    )


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