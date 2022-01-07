class TrainMetrics:
    header:list
    items:list

    def __init__(self, header, items=None) -> None:
        self.header = header
        self.items = items if items != None else list()
