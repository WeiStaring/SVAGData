from dataModel.BaseModel import *
from dataModel.VisualModel import *
def dataPipeline():
    washDataModel = WashDataModel()
    washDataModel.washData()

def analysis():
    analysisModel = AnalysisModel()
    analysisModel.checkStation()

analysis()