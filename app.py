from flask import Flask, render_template, request
from flask_livereload import LiveReload

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Do not use this in production
livereload = LiveReload(app)

@app.route("/")
def landingPage():
    return render_template('index.html')

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    if request.method == "POST":
        pass
    return render_template('login.html')

@app.route("/upload")
def upload_page():
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)