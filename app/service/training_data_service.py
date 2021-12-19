from app.datastore import Datastore

class TrainingDataService:
    def __init__(self, datastore:Datastore) -> None:
        self.datastore = datastore

    def getRuns(self):
        return self.datastore.getRuns()

    def getMetrics(self):
        return self.datastore.getMetrics()

    def getPlots(self, run=None):
        return self.datastore.getPlots(run)

    def getSummary(self):
        return self.datastore.getSummary()

    def getHyperparameters(self, run=None):
        return self.datastore.getHyperparameters(run)
