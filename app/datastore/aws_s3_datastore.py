import boto3
import json

from app.datastore import Datastore
from app.model import TrainMetrics, Metric, TrainPlots
from common.config import Config

class AwsS3Datastore(Datastore):
    def __init__(self, config:Config) -> None:
        self.bucket_name = config.storage_root
        self.bucket = boto3.resource("s3").Bucket(self.bucket_name)

    def getMetrics(self) -> TrainMetrics:
        header = []
        metrics = list()
        trainMetrics = TrainMetrics(header, metrics)
        return trainMetrics

    def getPlots(self) -> TrainPlots:
        plots = TrainPlots()
        return plots

    def getSummary(self):
        return json.loads("{}")

    def getHyperparameters(self):
        return json.loads("{}")

    def getRuns(self):
        runs = list()
        objectSummary = self.bucket.objects.all()
        for o in objectSummary:
            runs.append(o.key.split("/")[0])
        runs.sort(reverse=True)
        return runs
