import base64
import csv
import json
import io

from app.model.train_metrics import TrainMetrics
from app.model.train_plots import TrainPlots
from common import constants
from common.config import Config

class Datastore:
    def __init__(self, config:Config) -> None:
        self.config = config

    def getRuns(self):
        pass

    def getEvals(self, run):
        pass

    def getHyperparameters(self, run):
        pass

    def getSummary(self, run, eval):
        pass

    def getMetrics(self, run, eval):
        pass

    def getPlots(self, run, eval):
        pass

    def _get_runs_from_names(self, names):
        runs = [name.split("/")[0] for name in names]
        runs = sorted(set(runs), reverse=True)
        return runs

    def _get_evals_from_names(self, names, name_prefix):
        evals = [name.replace(name_prefix, "").split("/")[0] for name in names]
        evals = [int(e) for e in evals if e.isnumeric() and e != "0"]
        evals = sorted(set(evals), reverse=True)
        return evals

    def _get_hyperparameters_from_run(self, run):
        if run != None:
            blob_key = f"{run}/{self.config.hyperparameters_file}"
            hyperparams = self._get_blob_string(blob_key)
            return json.loads(hyperparams)

    def _get_summary_from_run(self, run, eval):
        if run != None and eval != None:
            blob_key = f"{run}/{self.config.epoch_directory}/{eval}/{self.config.summary_file}"
            summary = self._get_blob_string(blob_key)
            return json.loads(summary)

    def _get_metrics_from_run(self, run, eval):
        if run != None and eval != None:
            blob_key = f"{run}/{self.config.epoch_directory}/{eval}/{self.config.metrics_file}"
            blob_str = self._get_blob_string(blob_key)

            header = []
            items = list()
            with io.StringIO(blob_str) as fd:
                reader = csv.reader(fd)
                for i, row in enumerate(reader):
                    if i > 0:
                        items.append(row)
                    else:
                        header = row

            trainMetrics = TrainMetrics(header, items)
            return trainMetrics

    def _get_plots_from_run(self, run, eval):
        if run != None:
            plots = TrainPlots()
            blob_key = f"{run}/{self.config.target_samples_file}"
            blob_bytes = self._get_blob_bytes(blob_key)
            if blob_bytes != None:
                base64Value = base64.b64encode(blob_bytes).decode()
                plots.target = f"{self.config.plot_value_prefix}{base64Value}"

            if eval != None:
                blob_key = f"{run}/{self.config.epoch_directory}/{eval}/{self.config.loss_accuracy_file}"
                blob_bytes = self._get_blob_bytes(blob_key)
                if blob_bytes != None:
                    base64Value = base64.b64encode(blob_bytes).decode()
                    plots.loss = f"{self.config.plot_value_prefix}{base64Value}"

                blob_key = f"{run}/{self.config.epoch_directory}/{eval}/{self.config.generated_samples_file}"
                blob_bytes = self._get_blob_bytes(blob_key)
                if blob_bytes != None:
                    base64Value = base64.b64encode(blob_bytes).decode()
                    plots.image = f"{self.config.plot_value_prefix}{base64Value}"

            return plots

    def _get_blob_string(self, key):
        blob_bytes = self._get_blob_bytes(key)
        return blob_bytes.decode()

    def _get_blob_bytes(self, key):
        pass # not implemented in this abstract class

    @staticmethod
    def get_default_value(key):
        if key == constants.EVALS:
            return []
        elif key == constants.HYPERPARAMETERS:
            return json.loads("{}")
        elif key == constants.METRICS:
            return TrainMetrics([], list())
        elif key == constants.PLOTS:
            return TrainPlots()
        elif key == constants.RUNS:
            return []
        elif key == constants.SUMMARY:
            return json.loads("{}")
        
