import os
import json
from flask import Flask, request, render_template, Blueprint, session, jsonify, redirect, url_for
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath
from engine.vision_model import visionModel
from engine.dataAcquisition import dataAcquision

def register_acquire_page(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()
    vision_model = visionModel()
    dataAcquire = dataAcquision()

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

            result = vision_model.engine(image_path, prompt)

            # print(result)
            # print("AI Result:")

            if result is None:
                return render_template("acquireInfo.html", user=user, user_image = user_image, user_var = user_var, profile_image=profile_image,profile_name = profile_data[0],error="Unable to generate a valid diagnosis.", account_or_upload="upload",)

            folderHandler.saveJsonFile(vision_model.result)
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