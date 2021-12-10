from app.datastore import Datastore
from app.model import TrainMetrics, Metric

class TestDatastore(Datastore):
    def getMetrics(self):
        header = ["Epoch", "Mini-Batch", "Discriminator Loss: Real", "Discriminator Loss: Fake", "GAN Loss"]

        metrics = list()
        metrics.append(Metric(1, "0/234", 0.304, 2.544, 0.487))
        metrics.append(Metric(1, "1/234", 0.239, 1.219, 0.880))
        metrics.append(Metric(1, "1/234", 0.239, 1.219, 0.880))

        trainMetrics = TrainMetrics(header, metrics)

        return trainMetrics
