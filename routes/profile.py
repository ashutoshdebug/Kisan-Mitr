from flask import Flask, redirect, render_template, url_for, session, request, jsonify
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath
from pathlib import Path

def register_profile_page(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()

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