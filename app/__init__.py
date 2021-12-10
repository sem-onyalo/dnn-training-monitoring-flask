from flask import Flask, Blueprint, render_template
from app.datastore import TestDatastore
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

def init_app():
    global trainingDataService
    datastore = TestDatastore() # TODO: set value based on run param
    trainingDataService = TrainingDataService(datastore)

    app = Flask(__name__)
    app.register_blueprint(public)
    return app
