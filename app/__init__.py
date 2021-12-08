from flask import Flask, Blueprint

public = Blueprint("routes", __name__)

@public.route("/")
def default():
    return "...app is running..."

def init_app():
    app = Flask(__name__)
    app.register_blueprint(public)
    return app