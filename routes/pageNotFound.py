from flask import Flask, render_template

def register_pageNotFound_page(app):

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template("pageNotFound.html"), 404
