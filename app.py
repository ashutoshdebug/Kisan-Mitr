import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from flask_livereload import LiveReload
from database.db_handler import dbHandler
from engine.dataAcquisition import dataAcquision
from utils.filenFolderPath import fileFolderPath
from dotenv import load_dotenv
from engine.vision_model import visionModel


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["TEMPLATES_AUTO_RELOAD"] = True

livereload = LiveReload(app)

databaseHandler = dbHandler()
folderHandler = fileFolderPath()
visionModel = visionModel()
dataAcquire = dataAcquision()


ALLOWED_PROFILE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

DEFAULT_PROFILE_IMAGE = "uploads/frontend/default-profile.svg"


@app.context_processor
def profile_context():
    if (
        not databaseHandler.login_successful
        or not databaseHandler.username
    ):
        return {}

    username = databaseHandler.username
    profile = databaseHandler.getUserProfile(username)

    if not profile:
        databaseHandler.createUserProfile(username)
        profile = databaseHandler.getUserProfile(username)

    if not profile:
        return {
            "user_var": f"Hi {username}!",
            "account_or_upload": "upload",
            "username": username,
            "profile_name": username,
            "profile_email": "",
            "profile_image": DEFAULT_PROFILE_IMAGE
        }

    return {
        "user_var": f"Hi {username}!",
        "account_or_upload": "upload",
        "username": username,
        "profile_name": profile.get("name") or username,
        "profile_email": profile.get("email") or "",
        "profile_image": (
            profile.get("profile_image")
            or DEFAULT_PROFILE_IMAGE
        )
    }


@app.route("/")
def landingPage():
    if databaseHandler.login_successful:
        msg = f"Hi {databaseHandler.username}!"

        return render_template(
            "index.html",
            user_var=msg,
            account_or_upload="upload"
        )

    return render_template(
        "index.html",
        account_or_upload="account_page"
    )


@app.route("/logout", methods=["GET", "POST"])
def logout():
    data = request.get_json()
    logout = data.get("logout")

    if logout == True:
        databaseHandler.login_successful = False

    return jsonify({"status": "success"}), 200


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("pageNotFound.html"), 404


@app.route("/motive")
def motivePage():
    if databaseHandler.login_successful:
        msg = f"Hi {databaseHandler.username}!"

        return render_template(
            "motive.html",
            user_var=msg,
            account_or_upload="upload"
        )

    return render_template(
        "motive.html",
        account_or_upload="account_page"
    )


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

            databaseHandler.userRegistration(
                signup_name,
                signup_username,
                signup_email,
                signup_password
            )

            if databaseHandler.user_already_exist is True:
                return jsonify({
                    "user_already_exist": True
                })

            return redirect(
                url_for("account_page")
            )

        elif form_type == "login_form":
            login_email = request.form.get("login_email")
            login_password = request.form.get("login_password")

            print("Login email:", login_email)
            print("Login password:", login_password)

            databaseHandler.verifyUser(
                login_password,
                login_email
            )

            if databaseHandler.user_not_exist is True:
                return jsonify({
                    "not_exist": True
                }), 200

            if databaseHandler.login_successful:
                folderHandler.createFolder(
                    databaseHandler.username
                )

                return redirect(
                    url_for("upload")
                )

    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not databaseHandler.login_successful:
        return redirect(
            url_for("account_page")
        )

    username = databaseHandler.username

    if request.method == "POST":
        data = request.get_json(
            silent=True
        ) or {}

        if data.get("remove_image") is True:
            current_profile = (
                databaseHandler.getUserProfile(username)
            )

            old_image = (
                current_profile.get("profile_image")
                if current_profile
                else None
            )

            databaseHandler.saveProfileImage(
                username,
                DEFAULT_PROFILE_IMAGE
            )

            if old_image and old_image.startswith(
                "uploads/profiles/"
            ):
                old_file_path = os.path.join(
                    app.root_path,
                    "static",
                    old_image.replace("/", os.sep)
                )

                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)

            return jsonify({
                "status": "success"
            }), 200

        file = request.files.get("profile_image")

        if not file or file.filename == "":
            return redirect(url_for("profile"))

        original_name = secure_filename(
            file.filename
        )

        if not original_name or "." not in original_name:
            return redirect(url_for("profile"))

        extension = (
            original_name
            .rsplit(".", 1)[1]
            .lower()
        )

        if extension not in ALLOWED_PROFILE_EXTENSIONS:
            return redirect(url_for("profile"))

        safe_username = secure_filename(username)

        if not safe_username:
            return redirect(url_for("profile"))

        profile_dir = os.path.join(
            app.root_path,
            "static",
            "uploads",
            "profiles"
        )

        os.makedirs(profile_dir, exist_ok=True)

        current_profile = (
            databaseHandler.getUserProfile(username)
        )

        old_image = (
            current_profile.get("profile_image")
            if current_profile
            else None
        )

        filename = f"{safe_username}.{extension}"
        file_path = os.path.join(
            profile_dir,
            filename
        )

        file.save(file_path)

        profile_image_path = (
            f"uploads/profiles/{filename}"
        )

        databaseHandler.saveProfileImage(
            username,
            profile_image_path
        )

        if (
            old_image
            and old_image.startswith(
                "uploads/profiles/"
            )
            and old_image != profile_image_path
        ):
            old_file_path = os.path.join(
                app.root_path,
                "static",
                old_image.replace("/", os.sep)
            )

            if os.path.isfile(old_file_path):
                os.remove(old_file_path)

        return redirect(url_for("profile"))

    profile_data = databaseHandler.getUserProfile(
        username
    )

    if not profile_data:
        databaseHandler.createUserProfile(username)
        profile_data = databaseHandler.getUserProfile(
            username
        )

    if not profile_data:
        profile_data = {
            "name": username,
            "email": "",
            "profile_image": DEFAULT_PROFILE_IMAGE
        }

    return render_template(
        "profile.html",
        profile=profile_data
    )


@app.route("/result")
def results():
    if not databaseHandler.login_successful:
        return redirect(
            url_for("account_page")
        )

    msg = f"Hi {databaseHandler.username}!"

    if not visionModel.result_generated:
        return redirect(
            url_for("upload")
        )

    return render_template(
        "result.html",
        account_or_upload="upload",
        user_var=msg
    )


@app.route("/acquire", methods=["GET", "POST"])
def acquire():
    if not databaseHandler.login_successful:
        return redirect(
            url_for("account_page")
        )

    msg = f"Hi {databaseHandler.username}!"

    session["username"] = databaseHandler.username
    session["user-image"] = databaseHandler.imagePath

    if (
        session["username"] is None
        or session["user-image"] is None
    ):
        return redirect(
            url_for("upload")
        )

    user = session["username"]
    user_image = session["user-image"]

    static_path = os.path.join(
        app.root_path,
        "static"
    )

    user_image = os.path.relpath(
        user_image,
        static_path
    ).replace("\\", "/")

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

        prompt = dataAcquire.allFields(
            location,
            crop_season,
            temperature,
            humidity,
            rainfall,
            windspeed,
            variety,
            irrigation,
            soil,
            symptoms
        )

        databaseHandler.insertCropProperties(
            databaseHandler.username,
            location,
            crop_season,
            temperature,
            humidity,
            rainfall,
            windspeed,
            variety,
            irrigation,
            soil,
            symptoms
        )

        image_path = databaseHandler.getImagePath(
            databaseHandler.username
        )

        result = visionModel.engine(
            image_path,
            prompt
        )

        if result is None:
            return render_template(
                "acquireInfo.html",
                user=user,
                user_image=user_image,
                user_var=msg,
                error="Unable to generate a valid diagnosis.",
                account_or_upload="upload"
            )

        folderHandler.saveJsonFile(
            visionModel.result
        )

        databaseHandler.addResultName(
            databaseHandler.username,
            folderHandler.result_file
        )

        databaseHandler.getResultFilePath(
            databaseHandler.username
        )

        try:
            with open(
                databaseHandler.resultPath,
                "r",
                encoding="utf-8"
            ) as file:
                result = json.load(file)

        except (
            OSError,
            TypeError,
            json.JSONDecodeError
        ) as err:
            print("JSON open err:", err)
            return False

        return render_template(
            "result.html",
            user=user,
            user_image=user_image,
            result=result,
            user_var=msg,
            account_or_upload="upload"
        )

    return render_template(
        "acquireInfo.html",
        user=user,
        user_image=user_image,
        user_var=msg,
        account_or_upload="upload"
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not databaseHandler.login_successful:
        return redirect(
            url_for("account_page")
        )

    msg = f"Hi {databaseHandler.username}!"

    if request.method == "POST":
        file = request.files["fileInput"]

        if file.filename == "":
            print("No selected file")
            return redirect(request.url)

        if file:
            folderHandler.fileSave(file)

            databaseHandler.addImageName(
                databaseHandler.username,
                folderHandler.new_name
            )

            databaseHandler.getImagePath(
                databaseHandler.username
            )

            return redirect(
                url_for("acquire")
            )

    return render_template(
        "upload.html",
        user_var=msg,
        account_or_upload="upload"
    )