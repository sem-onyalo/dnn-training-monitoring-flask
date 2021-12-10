from app.datastore import Datastore

class TrainingDataService:
    def __init__(self, datastore:Datastore) -> None:
        self.datastore = datastore

    def getMetrics(self):
        return self.datastore.getMetrics()

    def getPlots(self):
        return self.datastore.getPlots()

    def getSummary(self):
        return self.datastore.getSummary()

    def getHyperparameters(self):
        return self.datastore.getHyperparameters()

    def getRuns(self):
        return self.datastore.getRuns()
