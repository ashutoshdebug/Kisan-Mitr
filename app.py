import os
from flask import Flask
from flask_livereload import LiveReload
from dotenv import load_dotenv


from routes.landing import register_landing_page
from routes.logout import register_logout_page
from routes.pageNotFound import register_pageNotFound_page
from routes.motivePage import register_motivePage
from routes.login import register_login_page
from routes.profile import register_profile_page
from routes.results import register_result_page
from routes.acquire import register_acquire_page
from routes.upload import register_upload_page


load_dotenv()  # To load env secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

in_development = os.getenv("in_development") == "True"

# Do not use this in production
if in_development:
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    livereload = LiveReload(app)

else:
    app.config["TEMPLATES_AUTO_RELOAD"] = False

register_landing_page(app)
register_logout_page(app)
register_pageNotFound_page(app)
register_motivePage(app)
register_login_page(app)
register_profile_page(app)
register_result_page(app)
register_acquire_page(app)
register_upload_page(app)