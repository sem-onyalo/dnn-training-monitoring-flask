import os

DEBUG_KEY = "DNN_TRAINING_DEBUG"
HOST_KEY = "DNN_TRAINING_HOST"
PORT_KEY = "DNN_TRAINING_PORT"
STORAGE_KEY = "DNN_TRAINING_STORAGE"
STORAGE_ROOT_KEY = "DNN_TRAINING_STORAGE_ROOT"
AUTO_REFRESH_SECONDS = "AUTO_REFRESH_SECONDS"

EPOCH_DIRECTORY = "EPOCH_DIRECTORY"
GENERATED_SAMPLES_FILE = "GENERATED_SAMPLES_FILE"
HYPERPARAMETERS_FILE = "HYPERPARAMETERS_FILE"
LOSS_ACCURACY_FILE = "LOSS_ACCURACY_FILE"
METRICS_FILE = "METRICS_FILE"
MODEL_FILE = "MODEL_FILE"
SUMMARY_FILE = "SUMMARY_FILE"
TARGET_SAMPLES_FILE = "TARGET_SAMPLES_FILE"

PLOT_VALUE_PREFIX = "PLOT_VALUE_PREFIX"

class Config:
    debug:bool
    host:str
    port:str
    storage:str
    storage_name:str

    def __init__(self, runtime_args) -> None:
        self.debug = os.environ.get(DEBUG_KEY, runtime_args.debug)
        self.host = os.environ.get(HOST_KEY, runtime_args.host_ip)
        self.port = os.environ.get(PORT_KEY, runtime_args.host_port)
        self.storage = os.environ.get(STORAGE_KEY, runtime_args.storage)
        self.storage_name = os.environ.get(STORAGE_ROOT_KEY, runtime_args.storage_name)
        self.auto_refresh_seconds = os.environ.get(AUTO_REFRESH_SECONDS, runtime_args.auto_refresh_seconds)

        self.epoch_directory = os.environ.get(EPOCH_DIRECTORY, "epoch")
        self.generated_samples_file = os.environ.get(GENERATED_SAMPLES_FILE, "generated.png")
        self.hyperparameters_file = os.environ.get(HYPERPARAMETERS_FILE, "hyperparameters.json")
        self.loss_accuracy_file = os.environ.get(LOSS_ACCURACY_FILE, "loss_accuracy.png")
        self.metrics_file = os.environ.get(METRICS_FILE, "metrics.csv")
        self.model_file = os.environ.get(MODEL_FILE, "model.h5")
        self.summary_file = os.environ.get(SUMMARY_FILE, "summary.json")
        self.target_samples_file = os.environ.get(TARGET_SAMPLES_FILE, "target.png")

        self.plot_value_prefix = os.environ.get(PLOT_VALUE_PREFIX, "data:image/png;base64,")
