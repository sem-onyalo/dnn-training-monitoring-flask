import io
import logging

from .datastore import Datastore
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from common.config import Config

class DatastoreAzureStorage(Datastore):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        credential = DefaultAzureCredential()
        account_url = f"https://{config.cloud_storage_account}.blob.core.windows.net"
        self.client = ContainerClient(account_url, config.storage_name, credential=credential)

    def getRuns(self):
        blobs_list = self.client.list_blobs()
        names = [item.name for item in blobs_list]
        return self._get_runs_from_names(names)

    def getEvals(self, run):
        blob_key = f"{run}/{self.config.epoch_directory}/"
        blobs_list = self.client.list_blobs(name_starts_with=blob_key)
        names = [item.name for item in blobs_list]
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
            blob_data = self.client.download_blob(key)
            blob_data.readinto(buffer)
            return buffer.getvalue()
        except ResourceNotFoundError as e:
            logging.error(f"Error while attempting to read blob {key}: {e}")
