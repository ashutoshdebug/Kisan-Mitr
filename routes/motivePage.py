from flask import Flask, redirect, render_template, Blueprint, session, current_app
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath

def register_motivePage(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()
    
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