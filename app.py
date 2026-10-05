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
from routes.results import register_result_page
from routes.acquire import register_acquire_page
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
register_result_page(app)
register_acquire_page(app)



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
            folderHandler.createFolder(username)
            folderHandler.fileSave(file)
            # print("File path committed")
            databaseHandler.addImageName(
                username, folderHandler.new_name
            )
            databaseHandler.getImagePath(username)
            return redirect(url_for("acquire"))

    return render_template("upload.html", user_var= user_var, profile_image=profile_image, profile_name = profile_data[0], account_or_upload="upload")