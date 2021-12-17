import os

DEBUG_KEY = "DNN_TRAINING_DEBUG"
HOST_KEY = "DNN_TRAINING_HOST"
PORT_KEY = "DNN_TRAINING_PORT"
STORAGE_KEY = "DNN_TRAINING_STORAGE"
STORAGE_ROOT_KEY = "DNN_TRAINING_STORAGE_ROOT"

class Config:
    debug:bool
    host:str
    port:str
    storage:str
    storage_root:str

    def __init__(self, runtime_args) -> None:
        self.debug = os.environ.get(DEBUG_KEY, runtime_args.debug)
        self.host = os.environ.get(HOST_KEY, runtime_args.host_ip)
        self.port = os.environ.get(PORT_KEY, runtime_args.host_port)
        self.storage = os.environ.get(STORAGE_KEY, runtime_args.storage)
        self.storage_root = os.environ.get(STORAGE_ROOT_KEY, runtime_args.storage_root)
