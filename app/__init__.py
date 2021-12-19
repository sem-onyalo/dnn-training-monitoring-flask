from flask import Flask, Blueprint, render_template
from app.datastore import TestDatastore, AwsS3Datastore
from app.service import TrainingDataService

public = Blueprint("routes", __name__)
trainingDataService = None

@public.route("/", defaults={"run": None})
def default(run):
    runs = trainingDataService.getRuns()
    if run == None and len(runs) > 0:
        run = runs[0]

    hyperparams = trainingDataService.getHyperparameters(run)
    metrics = trainingDataService.getMetrics()
    plots = trainingDataService.getPlots(run)
    summary = trainingDataService.getSummary()

    return render_template(
        "index.html", 
        metrics=metrics, 
        plots=plots, 
        summary=summary, 
        hyperparams=hyperparams,
        runs=runs,
        currentRun=run)

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
