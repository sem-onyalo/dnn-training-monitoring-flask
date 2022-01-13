from common import constants
from common.config import Config
from flask import Flask, Blueprint, render_template
from app.datastore import get_datastore, get_default_value
from app.service import TrainingDataService

public = Blueprint("routes", __name__)

auto_refresh_seconds:int = None
trainingDataService:TrainingDataService = None

@public.route("/", defaults={"run": None, "eval": None})
@public.route("/<run>", defaults={"eval": None})
@public.route("/<run>/<eval>")
def default(run, eval):
    runs = get_runs()
    
    run = get_current_run(runs, run)
    hyperparams = get_hyperparameters(run)
    evals = get_evals(run)

    eval = get_current_eval(evals, eval)
    plots = get_plots(run, eval)
    metrics = get_metrics(run, eval)
    summary = get_summary(run, eval)

    return render_template(
        "index.html",
        auto_refresh_seconds=auto_refresh_seconds,
        metrics=metrics,
        plots=plots,
        summary=summary,
        hyperparams=hyperparams,
        runs=runs,
        currentRun=run,
        evals=evals,
        currentEval=eval)

def init_app(config:Config):
    global auto_refresh_seconds
    auto_refresh_seconds = config.auto_refresh_seconds

    global trainingDataService
    datastore = get_datastore(config)
    trainingDataService = TrainingDataService(datastore)

    app = Flask(__name__)
    app.register_blueprint(public)
    return app

def get_evals(run): 
    evals = trainingDataService.getEvals(run)
    return evals if evals != None else get_default_value(constants.EVALS)

def get_hyperparameters(run): 
    params = trainingDataService.getHyperparameters(run)
    return params if params != None else get_default_value(constants.HYPERPARAMETERS)

def get_metrics(run, eval): 
    metrics = trainingDataService.getMetrics(run, eval)
    return metrics if metrics != None else get_default_value(constants.METRICS)

def get_plots(run, eval): 
    plots = trainingDataService.getPlots(run, eval)
    return plots if plots != None else get_default_value(constants.PLOTS)

def get_runs(): 
    runs = trainingDataService.getRuns()
    return runs if runs != None else get_default_value(constants.RUNS)

def get_summary(run, eval): 
    summary = trainingDataService.getSummary(run, eval)
    return summary if summary != None else get_default_value(constants.SUMMARY)

def get_current_run(runs, run):
    if run == None and len(runs) > 0:
        run = runs[0]
    return run

def get_current_eval(evals, eval):
    if eval == None and len(evals) > 0:
        eval = evals[0]
    return eval