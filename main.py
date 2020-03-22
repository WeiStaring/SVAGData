from dataModel.BaseModel import *
from dataModel.SpaceVolumeModel import *
from dataModel.VisualModel import *
from dataModel.SpaceFlowModel import *


def modelPipeline():
    # washDataModel = WashDataModel()
    # washDataModel.washData()
    # washDataModel.station2box()
    # spaceVolumeModel = SpaceVolumeModel()
    # spaceVolumeModel.dataPipeline()
    spaceFlowModel = SpaceFlowModel()
    spaceFlowModel.dataPipeline()

def analysis():
    analysisModel = AnalysisModel()
    # analysisModel.checkStation()
    # analysisModel.processStation()
    # analysisModel.checkRecords()
    analysisModel.checkTrip1()

analysis()