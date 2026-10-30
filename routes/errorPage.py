from flask import Flask, request, redirect, render_template, session, url_for

def register_error_page(app):

    @app.route("/error", methods=["GET"])
    def error_page():

        # Prevent direct URL access
        if not session.pop("allow_error_page", False):
            return redirect(url_for("landingPage"))

        return render_template("errorpage.html")
