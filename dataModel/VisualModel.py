import matplotlib.pyplot as plt
from dataModel.BaseModel import *
import math


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
        station = pd.read_csv(self.dataDir + 'station.csv', dtype={'longitude': str, 'latitude': str})
        station['newPlot'] = -1
        index = 0
        print(station.info())
        dic = {}
        for i in range(len(station)):
            lon = station.iloc[i]['longitude']
            lat = station.iloc[i]['latitude']
            if not dic.__contains__((lon, lat)):
                dic[(lon, lat)] = index
                station.iloc[i, 3] = index
                index += 1
            else:
                station.iloc[i, 3] = dic[(lon, lat)]

        print(station.info())
        station.to_csv(self.resultDataDir + 'drop_duplicates_station.csv', index=False)

    def checkStation(self):
        """
        基站空间分布分析
        :return:
        """
        # df = pd.read_csv('data/dataAfterWash.csv')
        station = pd.read_csv(self.dataDir + 'station.csv', dtype={'longitude': str, 'latitude': str})
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

    def checkTripMode(self):
        df = pd.read_csv(self.finalDir + 'TripModeResult.csv')
        dic = {1: 'red', 2: 'green', 3: 'pink', 4: 'blue'}
        for name, gp in df.groupby(['imsi']):
            print(gp.iloc[:, 5:10])
            x = []
            y = []
            z = []
            for j in range(len(gp) - 1):
                sub = gp.iloc[j]
                x.append([sub['startlatitude'], sub['endlatitude']])
                y.append([sub['startlongitude'], sub['endlongitude']])
                z.append(sub['type'])
            print(x, y)
            for i in range(len(x)):
                plt.scatter(x[i], y[i], color='black', s=5)
                plt.arrow(x[i][0], y[i][0], x[i][1] - x[i][0], y[i][1] - y[i][0], width=0.0002,
                          length_includes_head=True,
                          head_width=0.005, head_length=0.005, fc='k', ec='k', lw=0.02, alpha=0.75, color='red')
                plt.plot(x[i], y[i], color=dic[z[i]], label='sin')

            plt.show()

    def checkTrip1(self):
        def rad(d):
            return d * 3.14 / 180.0

        def getDistance(x):
            EARTH_REDIUS = 6378.137
            lat1, lng1, lat2, lng2 = x['latitude'], x['longitude'], x['nextLat'], x['nextLon']
            radLat1 = rad(lat1)
            radLat2 = rad(lat2)
            a = radLat1 - radLat2
            b = rad(lng1) - rad(lng2)
            s = 2 * math.asin(
                math.sqrt(
                    math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2),
                                                                                                    2)))
            s = s * EARTH_REDIUS
            return s

        # df = pd.read_csv(self.resultDataDir + 'clusterRes.csv')
        # res = pd.DataFrame([],columns=['newPlot','cluster','usedTime','distance','speed'])
        # for name,gp in df.groupby(['imsi']):
        #     gp['nextTime'] = gp['date_time'].shift(1)
        #     gp['nextLon'] = gp['longitude'].shift(1)
        #     gp['nextLat'] = gp['latitude'].shift(1)
        #     gp['usedTime'] = (gp['date_time']-gp['nextTime'])/1000
        #     gp['distance'] = gp.apply(getDistance, axis=1)
        #     gp['distance']*=1000
        #     gp = gp.drop(['imsi','nextTime','date_time','nextLon','nextLat','longitude','latitude'],axis=1)
        #     gp['speed'] = gp['distance']/gp['usedTime']
        #     gp = gp[1:]
        #     res = pd.concat([res,gp],axis=0,ignore_index=True)
        # res.to_csv(self.resultDataDir+'forAnalysis.csv',index=False)

        df2 = pd.read_csv(self.resultDataDir + 'forAnalysis.csv')
        df2['speed']/=3.6
        df2 = df2[(df2['speed']<100) & (df2['speed']>0.1)]
        df2.hist('speed',bins=20)
        plt.show()
        df2.hist('usedTime', bins=20)
        plt.show()
        df2.hist('distance', bins=20)
        plt.show()



    def checkTrip(self):
        df = pd.read_csv(self.finalDir + 'TripModeResult.csv')
        df['usedTime'] = (df['end'] - df['start']) / 1000
        EARTH_REDIUS = 6378.137

        def rad(d):
            return d * 3.14 / 180.0

        def getDistance(x):
            lat1, lng1, lat2, lng2 = x['startlatitude'], x['startlongitude'], x['endlatitude'], x['endlongitude']
            radLat1 = rad(lat1)
            radLat2 = rad(lat2)
            a = radLat1 - radLat2
            b = rad(lng1) - rad(lng2)
            s = 2 * math.asin(
                math.sqrt(
                    math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2),
                                                                                                    2)))
            s = s * EARTH_REDIUS
            return s

        df['distance'] = df.apply(getDistance, axis=1)
        df['distance'] *= 1000
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        temp1 = df[df['type'] == 3]
        temp2 = df[df['type'] == 4]
        ax.scatter(temp1['distance'], temp1['usedTime'], c='red')
        ax.scatter(temp2['distance'], temp2['usedTime'], c='blue')
        plt.legend(["ride","bus"])
        ax.set_xlabel('disrance(m)')
        ax.set_ylabel('time(s)')
        plt.show()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        temp3 = df['distance'] / df['usedTime']
        ax.scatter([x for x in range(len(temp3))], temp3, c='red')
        ax.set_xlabel('index')
        ax.set_ylabel('speed(m/s)')
        plt.show()
