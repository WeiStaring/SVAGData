import matplotlib.pyplot as plt
from dataModel.BaseModel import *


class VisualModel(BaseModel):
    def __init__(self):
        super().__init__()

    def scatter(self,x,y,c):
        plt.scatter(x,y,c=c)
        plt.show()

class AnalysisModel(VisualModel):
    def __init__(self):
        super().__init__()

    def checkStation(self):
        df = pd.read_csv('data/dataAfterWash.csv')
        station = pd.read_csv('data/station.csv')
        c = []
        for i in range(len(station)):
            sum = np.sum(df['laci'] == station.iloc[i]['laci'])
            c.append(sum)
        c = np.array(c)
        print(np.sum(c>10))
        statis = pd.DataFrame(c,columns=['records'])
        statis['records'].hist(bins=50)
        plt.show()
        self.scatter(station['longitude'], station['latitude'], c)