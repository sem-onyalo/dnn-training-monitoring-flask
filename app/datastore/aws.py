import boto3
import io
import logging

from .datastore import Datastore
from botocore.exceptions import ClientError
from common.config import Config

class DatastoreAwsS3(Datastore):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.bucket = boto3.resource("s3").Bucket(config.storage_name)

    def getRuns(self):
        object_summary = self.bucket.objects.all()
        names = [item.key for item in object_summary]
        return self._get_runs_from_names(names)

    def getEvals(self, run):
        blob_key = f"{run}/{self.config.epoch_directory}/"
        object_summary = self.bucket.objects.filter(Prefix=blob_key)
        names = [item.key for item in object_summary]
        return self._get_evals_from_names(names, blob_key)

    def getHyperparameters(self, run):
        return self._get_hyperparameters_from_run(run)

    def getSummary(self, run, eval):
        return self._get_summary_from_run(run, eval)

    def getMetrics(self, run, eval):
        return self._get_metrics_from_run(run, eval)

    def getPlots(self, run, eval):
        return self._get_plots_from_run(run, eval)

    def _get_blob_bytes(self, key):
        try:
            buffer = io.BytesIO()
            self.bucket.download_fileobj(key, buffer)
            return buffer.getvalue()
        except ClientError as e:
            logging.error(f"Error while attempting to read blob {key}: {e}")
