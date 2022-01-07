from .aws import DatastoreAwsS3
from .test import DatastoreTest

def get_datastore(config):
    if config.storage == "aws_s3":
        return DatastoreAwsS3(config)
    elif config.storage == "test":
        return DatastoreTest()
    else:
        raise Exception(f"Unsupported storage type: {config.storage}")
