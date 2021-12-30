import base64
import boto3
import csv
import io
import json
import logging

from app.datastore import Datastore
from app.model import TrainMetrics, Metric, TrainPlots
from botocore.exceptions import ClientError
from common.config import Config

EPOCH_PREFIX = "epoch"
PLOT_VALUE_PREFIX = "data:image/png;base64,"
TARGET_PLOT_FILE_NAME = "target.png"
GENERATED_PLOT_FILE_NAME = "generated.png"
LOSS_ACCURACY_FILE_NAME = "loss_accuracy.png"
METRICS_FILE_NAME = "metrics.csv"
SUMMARY_FILE_NAME = "summary.json"
HYPERPARAMETERS_FILE_NAME = "hyperparameters.json"

class AwsS3Datastore(Datastore):
    def __init__(self, config:Config) -> None:
        self.bucket_name = config.storage_root
        self.bucket = boto3.resource("s3").Bucket(self.bucket_name)

    def getRuns(self):
        objectSummary = self.bucket.objects.all()
        runs = [o.key.split("/")[0] for o in objectSummary]
        runs = sorted(set(runs), reverse=True)
        return runs

    def getEvals(self, run):
        epochPrefixKey = f"{run}/{EPOCH_PREFIX}/"
        objectSummary = self.bucket.objects.filter(Prefix=epochPrefixKey)
        evals = [o.key.replace(epochPrefixKey, "").split("/")[0] for o in objectSummary]
        evals = [int(e) for e in evals if e.isnumeric()]
        evals = sorted(set(evals), reverse=True)
        return evals

    def getHyperparameters(self, run):
        hyperparams = "{}"
        if run != None:
            blob_key = f"{run}/{HYPERPARAMETERS_FILE_NAME}"
            hyperparams = self._get_blob_string(blob_key)

        return json.loads(hyperparams)

    def getSummary(self, run, eval):
        summary = "{}"
        if run != None and eval != None:
            blob_key = f"{run}/{EPOCH_PREFIX}/{eval}/{SUMMARY_FILE_NAME}"
            summary = self._get_blob_string(blob_key)

        return json.loads(summary)

    def getMetrics(self, run, eval):
        header = []
        metrics = list()
        if run != None and eval != None:
            blob_key = f"{run}/{EPOCH_PREFIX}/{eval}/{METRICS_FILE_NAME}"
            blob_str = self._get_blob_string(blob_key)

            with io.StringIO(blob_str) as fd:
                reader = csv.reader(fd)
                for i, row in enumerate(reader):
                    if i > 0:
                        epoch = row[0]
                        epochs = row[1]
                        mini_batch = row[2]
                        mini_batches = row[3]
                        d_loss_real = row[4]
                        d_loss_fake = row[5]
                        g_loss = row[6]
                        metric = Metric(epoch, epochs, mini_batch, mini_batches, d_loss_real, d_loss_fake, g_loss)
                        metrics.insert(0, metric)
                    else:
                        header = row

                    i += 1

        trainMetrics = TrainMetrics(header, metrics)
        return trainMetrics

    def getPlots(self, run, eval):
        plots = TrainPlots()
        if run != None:
            blob_key = f"{run}/{TARGET_PLOT_FILE_NAME}"
            blob_bytes = self._get_blob_bytes(blob_key)
            if blob_bytes != None:
                base64Value = base64.b64encode(blob_bytes).decode()
                plots.target = f"{PLOT_VALUE_PREFIX}{base64Value}"

            if eval != None:
                blob_key = f"{run}/{EPOCH_PREFIX}/{eval}/{LOSS_ACCURACY_FILE_NAME}"
                blob_bytes = self._get_blob_bytes(blob_key)
                if blob_bytes != None:
                    base64Value = base64.b64encode(blob_bytes).decode()
                    plots.loss = f"{PLOT_VALUE_PREFIX}{base64Value}"

                blob_key = f"{run}/{EPOCH_PREFIX}/{eval}/{GENERATED_PLOT_FILE_NAME}"
                blob_bytes = self._get_blob_bytes(blob_key)
                if blob_bytes != None:
                    base64Value = base64.b64encode(blob_bytes).decode()
                    plots.image = f"{PLOT_VALUE_PREFIX}{base64Value}"

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
