class Metric:
    epoch:int
    miniBatch:str
    dLossReal:float
    dLossFake:float
    gLoss:float

    def __init__(self, epoch, miniBatch, dLossReal, dLossFake, gLoss) -> None:
        self.epoch = epoch
        self.miniBatch = miniBatch
        self.dLossReal = dLossReal
        self.dLossFake = dLossFake
        self.gLoss = gLoss
