from app.datastore import Datastore

class TrainingDataService:
    def __init__(self, datastore:Datastore) -> None:
        self.datastore = datastore

    def getMetrics(self):
        return self.datastore.getMetrics()
