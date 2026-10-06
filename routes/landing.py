from flask import Flask, redirect, render_template, Blueprint, session, current_app
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath


def register_landing_page(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()

    @app.route("/", endpoint = "landingPage")
    def landingPage():
        if "username" in session:
            username = session["username"]
        # if databaseHandler.login_successful:
            user_var = True
            profile_data = databaseHandler.getProfileData(username)
            profile_image = folderHandler.getPFPImage(current_app.root_path, username)
            return render_template("index.html", user_var = user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload="upload")
        return render_template("index.html", account_or_upload="account_page")