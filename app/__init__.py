from flask import Flask, Blueprint, render_template

public = Blueprint("routes", __name__)

@public.route("/")
def default():
    return render_template("index.html")

def init_app():
    app = Flask(__name__)
    app.register_blueprint(public)
    return app