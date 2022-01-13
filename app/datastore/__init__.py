from .aws import DatastoreAwsS3
from .azure import DatastoreAzureStorage
from .datastore import Datastore
from .test import DatastoreTest

def get_datastore(config):
    if config.storage == "aws_s3":
        return DatastoreAwsS3(config)
    elif config.storage == "azure_storage":
        return DatastoreAzureStorage(config)
    elif config.storage == "test":
        return DatastoreTest()
    else:
        raise Exception(f"Unsupported storage type: {config.storage}")

def get_default_value(key):
    return Datastore.get_default_value(key)
