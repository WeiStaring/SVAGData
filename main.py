from dataModel.BaseModel import *
from dataModel.SpaceFlowModel import *
from dataModel.VisualModel import *

def modelPipeline():
    washDataModel = WashDataModel()
    washDataModel.washData()
    # spaceFlowModel = SpaceFlowModel()
    # spaceFlowModel.dataPipeline()

def analysis():
    analysisModel = AnalysisModel()
    # analysisModel.checkStation()
    analysisModel.checkRecords()

modelPipeline()