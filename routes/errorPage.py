from flask import Flask, request, redirect, render_template

def register_error_page(app):
    @app.route("/error", methods = ["GET"])
    def error_page():
        return render_template("errorpage.html")