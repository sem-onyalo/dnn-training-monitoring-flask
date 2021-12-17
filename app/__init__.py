from flask import Flask, Blueprint, render_template
from app.datastore import TestDatastore, AwsS3Datastore
from app.service import TrainingDataService

public = Blueprint("routes", __name__)
trainingDataService = None

@public.route("/")
def default():
    metrics = trainingDataService.getMetrics()
    plots = trainingDataService.getPlots()
    summary = trainingDataService.getSummary()
    hyperparams = trainingDataService.getHyperparameters()
    runs = trainingDataService.getRuns()

    return render_template(
        "index.html", 
        metrics=metrics, 
        plots=plots, 
        summary=summary, 
        hyperparams=hyperparams,
        runs=runs)

def init_app(config):
    global trainingDataService
    datastore = get_datastore(config)
    trainingDataService = TrainingDataService(datastore)

    app = Flask(__name__)
    app.register_blueprint(public)
    return app

def get_datastore(config):
    if config.storage == "aws_s3":
        return AwsS3Datastore(config)
    elif config.storage == "test":
        return TestDatastore()
    else:
        raise Exception(f"Unsupported storage type: {config.storage}")
