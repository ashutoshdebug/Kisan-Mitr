from flask import session, jsonify

def register_logout_page(app):
    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        session.clear()
        response = {"status": "success"}
        return jsonify(response), 200