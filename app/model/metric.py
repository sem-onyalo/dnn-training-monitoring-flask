class Metric:
    epoch:int
    epochs:int
    miniBatch:int
    miniBatches:int
    dLossReal:float
    dLossFake:float
    gLoss:float

    def __init__(self, epoch, epochs, miniBatch, miniBatches, dLossReal, dLossFake, gLoss) -> None:
        self.epoch = epoch
        self.epochs = epochs
        self.miniBatch = miniBatch
        self.miniBatches = miniBatches
        self.dLossReal = dLossReal
        self.dLossFake = dLossFake
        self.gLoss = gLoss
