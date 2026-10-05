from flask import Flask, request, render_template, Blueprint, session, jsonify, redirect, url_for
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath
from engine.vision_model import visionModel

def register_result_page(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()
    vision_Model = visionModel()

    @app.route("/result")
    def results():
        if "username" not in session:
            return redirect(url_for("account_page"))

        username = session["username"]
        # msg = f"Hi {databaseHandler.username}!"
        user_var = True
        profile_image = folderHandler.getPFPImage(app.root_path, username)
        profile_data = databaseHandler.getProfileData(username)

        if not vision_Model.result_generated:
            return redirect(url_for("upload"))

        return render_template("result.html", account_or_upload="upload", profile_image=profile_image, user_var = user_var, profile_name = profile_data[0])