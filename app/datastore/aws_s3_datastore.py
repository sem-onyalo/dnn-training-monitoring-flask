import base64
import boto3
import io
import json
import logging

from app.datastore import Datastore
from app.model import TrainMetrics, Metric, TrainPlots
from botocore.exceptions import ClientError
from common.config import Config

PLOT_VALUE_PREFIX = "data:image/png;base64,"
TARGET_PLOT_FILE_NAME = "target.png"
HYPERPARAMETERS_FILE_NAME = "hyperparameters.json"

class AwsS3Datastore(Datastore):
    def __init__(self, config:Config) -> None:
        self.bucket_name = config.storage_root
        self.bucket = boto3.resource("s3").Bucket(self.bucket_name)

    def getMetrics(self) -> TrainMetrics:
        header = []
        metrics = list()
        trainMetrics = TrainMetrics(header, metrics)
        return trainMetrics

    def getPlots(self, run=None) -> TrainPlots:
        plots = TrainPlots()
        if run != None:
            blobBytes = self._get_blob_bytes(f"{run}/{TARGET_PLOT_FILE_NAME}")
            if blobBytes != None:
                base64Value = base64.b64encode(blobBytes).decode()
                plots.target = f"{PLOT_VALUE_PREFIX}{base64Value}"

        return plots

    def getSummary(self):
        return json.loads("{}")

    def getHyperparameters(self, run=None):
        hyperparams = "{}"
        if run != None:
            blobBytes = self._get_blob_bytes(f"{run}/{HYPERPARAMETERS_FILE_NAME}")
            if blobBytes != None:
                hyperparams = blobBytes.decode()

        return json.loads(hyperparams)

    def getRuns(self):
        runs = list()
        objectSummary = self.bucket.objects.all()
        for o in objectSummary:
            runs.append(o.key.split("/")[0])
        runs = sorted(set(runs), reverse=True)
        return runs

    def _get_blob_bytes(self, key):
        try:
            buffer = io.BytesIO()
            self.bucket.download_fileobj(key, buffer)
            return buffer.getvalue()
        except ClientError as e:
            logging.error(f"Error while attempting to read blob {key}: {e}")
