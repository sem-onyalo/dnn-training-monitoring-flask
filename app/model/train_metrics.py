from app.model import Metric
from typing import List

class TrainMetrics:
    header:list
    metrics:List[Metric]

    def __init__(self, header, metrics=None) -> None:
        self.header = header
        self.metrics = metrics if metrics != None else list()
