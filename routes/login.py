from flask import Flask, request, render_template, Blueprint, session, jsonify, redirect, url_for
from database.db_handler import dbHandler
from utils.filenFolderPath import fileFolderPath

def register_login_page(app):
    databaseHandler = dbHandler()
    folderHandler = fileFolderPath()
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