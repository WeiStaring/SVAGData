import matplotlib.pyplot as plt
from dataModel.BaseModel import *


class VisualModel(BaseModel):
    def __init__(self):
        super().__init__()

    def scatter(self, x, y, c):
        plt.scatter(x, y, c=c)
        plt.show()


class AnalysisModel(VisualModel):
    def __init__(self):
        super().__init__()

    def processStation(self):
        """
        将位置相同的基站标上同样的类别记号
        :return:
        """
        station = pd.read_csv(self.dataDir+'station.csv', dtype={'longitude': str, 'latitude': str})
        station['newPlot'] = -1
        index = 0
        print(station.info())
        dic = {}
        for i in range(len(station)):
            lon = station.iloc[i]['longitude']
            lat = station.iloc[i]['latitude']
            if not dic.__contains__((lon, lat)):
                dic[(lon, lat)] = index
                station.iloc[i,3] = index
                index += 1
            else:
                station.iloc[i,3] = dic[(lon, lat)]

        print(station.info())
        station.to_csv(self.resultDataDir + 'drop_duplicates_station.csv', index=False)

    def checkStation(self):
        """
        基站空间分布分析
        :return:
        """
        # df = pd.read_csv('data/dataAfterWash.csv')
        station = pd.read_csv(self.dataDir+'station.csv', dtype={'longitude': str, 'latitude': str})
        print(station.info())
        # station['longitude'] = station['longitude'].astype(str)
        # station['latitude'] = station['latitude'].astype(str)
        station = station.drop_duplicates(['longitude', 'latitude'])
        print(station.info())

        # c = []
        # for i in range(len(station)):
        #     sum = np.sum(df['laci'] == station.iloc[i]['laci'])
        #     c.append(sum)
        # c = np.array(c)
        # print(np.sum(c>10))
        # statis = pd.DataFrame(c,columns=['records'])
        # statis['records'].hist(bins=50)
        # plt.show()
        # self.scatter(station['longitude'], station['latitude'], c)

    def checkRecords(self):
        df = pd.read_csv(self.resultDataDir + 'dataAfterWash.csv')
        df['timestamp'] -= 1538496000000
        df['timestamp'] /= 1000
        # 使用5分钟作为时间槽 9849->8179
        df['timestamp'] /= 60 * 5
        df['timestamp'] = df['timestamp'].astype(int)
        print(df.info())
        df = df.drop_duplicates(['timestamp', 'laci', 'imsi'])
        print(df.info())
        # df['timestamp'].hist(bins=288)
        # plt.show()
