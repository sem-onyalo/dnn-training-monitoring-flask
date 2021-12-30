from app.datastore import Datastore

class TrainingDataService:
    def __init__(self, datastore:Datastore) -> None:
        self.datastore = datastore

    def getRuns(self):
        return self.datastore.getRuns()

    def getEvals(self, run):
        return self.datastore.getEvals(run)

    def getHyperparameters(self, run):
        return self.datastore.getHyperparameters(run)

    def getSummary(self, run, eval):
        return self.datastore.getSummary(run, eval)

    def getMetrics(self, run, eval):
        return self.datastore.getMetrics(run, eval)

    def getPlots(self, run, eval):
        return self.datastore.getPlots(run, eval)
