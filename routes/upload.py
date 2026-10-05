from flask import Flask, request, render_template, Blueprint, session, jsonify, redirect, url_for
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath


def register_upload_page(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()

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