import base64
import boto3
import csv
import io
import json
import logging

from app.model import TrainMetrics, TrainPlots
from botocore.exceptions import ClientError
from common.config import Config

class DatastoreAwsS3:
    def __init__(self, config:Config) -> None:
        self.config = config
        self.bucket = boto3.resource("s3").Bucket(config.storage_name)

    def getRuns(self):
        objectSummary = self.bucket.objects.all()
        runs = [o.key.split("/")[0] for o in objectSummary]
        runs = sorted(set(runs), reverse=True)
        return runs

    def getEvals(self, run):
        epochPrefixKey = f"{run}/{self.config.epoch_directory}/"
        objectSummary = self.bucket.objects.filter(Prefix=epochPrefixKey)
        evals = [o.key.replace(epochPrefixKey, "").split("/")[0] for o in objectSummary]
        evals = [int(e) for e in evals if e.isnumeric()]
        evals = sorted(set(evals), reverse=True)
        return evals

    def getHyperparameters(self, run):
        hyperparams = "{}"
        if run != None:
            blob_key = f"{run}/{self.config.hyperparameters_file}"
            hyperparams = self._get_blob_string(blob_key)

        return json.loads(hyperparams)

    def getSummary(self, run, eval):
        summary = "{}"
        if run != None and eval != None:
            blob_key = f"{run}/{self.config.epoch_directory}/{eval}/{self.config.summary_file}"
            summary = self._get_blob_string(blob_key)

        return json.loads(summary)

    def getMetrics(self, run, eval):
        header = []
        items = list()
        if run != None and eval != None:
            blob_key = f"{run}/{self.config.epoch_directory}/{eval}/{self.config.metrics_file}"
            blob_str = self._get_blob_string(blob_key)

            with io.StringIO(blob_str) as fd:
                reader = csv.reader(fd)
                for i, row in enumerate(reader):
                    if i > 0:
                        items.append(row)
                    else:
                        header = row

        trainMetrics = TrainMetrics(header, items)
        return trainMetrics

    def getPlots(self, run, eval):
        plots = TrainPlots()
        if run != None:
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

    def _get_blob_bytes(self, key):
        try:
            buffer = io.BytesIO()
            self.bucket.download_fileobj(key, buffer)
            return buffer.getvalue()
        except ClientError as e:
            logging.error(f"Error while attempting to read blob {key}: {e}")

    def _get_blob_string(self, key):
        blob_bytes = self._get_blob_bytes(key)
        return blob_bytes.decode()
