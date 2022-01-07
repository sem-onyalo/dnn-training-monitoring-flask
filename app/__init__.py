from flask import Flask, Blueprint, render_template
from app.datastore import get_datastore
from app.service import TrainingDataService

public = Blueprint("routes", __name__)
trainingDataService:TrainingDataService = None

@public.route("/", defaults={"run": None, "eval": None})
@public.route("/<run>", defaults={"eval": None})
@public.route("/<run>/<eval>")
def default(run, eval):
    runs = trainingDataService.getRuns()
    if run == None and len(runs) > 0:
        run = runs[0]

    evals = trainingDataService.getEvals(run)
    if eval == None and len(evals) > 0:
        eval = evals[0]

    hyperparams = trainingDataService.getHyperparameters(run)
    plots = trainingDataService.getPlots(run, eval)
    metrics = trainingDataService.getMetrics(run, eval)
    summary = trainingDataService.getSummary(run, eval)

    return render_template(
        "index.html", 
        metrics=metrics, 
        plots=plots, 
        summary=summary, 
        hyperparams=hyperparams,
        runs=runs,
        currentRun=run,
        evals=evals,
        currentEval=eval)

def init_app(config):
    global trainingDataService
    datastore = get_datastore(config)
    trainingDataService = TrainingDataService(datastore)

    app = Flask(__name__)
    app.register_blueprint(public)
    return app
