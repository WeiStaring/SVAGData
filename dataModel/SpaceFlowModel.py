from dataModel.BaseModel import *
from utils.util import *
from utils.STDBSCAN import *
import warnings
import time

warnings.filterwarnings('ignore')


class SpaceFlowModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(self.resultDataDir + 'dataAfterWash.csv')
        self.station = pd.read_csv(self.finalDir + 'newStation.csv')
        self.station2box = self.loadJson(self.finalDir+'station2box.json')
        self.listType = self.df['imsi'].unique()
        self.userNum = self.listType.size

    def dataPipeline(self):
        # self.dataProcess()
        # self.getClusterDf()
        # self.getStay()
        # self.getTrip()
        self.aggregateStay()
        self.aggregateTrip()

    def dataProcess(self):
        # self.df['date_time'] = pd.to_datetime(self.df['timestamp'] + 28800000, unit='ms')
        self.df['date_time'] = self.df['timestamp']
        self.df.drop(['timestamp'], inplace=True, axis=1)

    def getClusterDf(self):
        # TODO 调参
        # STDBSCAN参数
        spatial_threshold = 1000  # meters
        temporal_threshold = 30  # minutes
        min_neighbors = 2

        # 按id划分用户
        listType = self.listType
        userNum = self.userNum

        # 聚类结果
        clusterDf = pd.DataFrame(columns=['imsi', 'longitude', 'latitude', 'newPlot', 'date_time', 'cluster'])

        for i in range(0, userNum):
            tempUser = self.df[self.df['imsi'].isin([listType[i]])]
            # 对每个用户的数据进行聚类
            df_clustering = ST_DBSCAN(tempUser, spatial_threshold, temporal_threshold, min_neighbors)
            clusterDf = clusterDf.append(df_clustering)

        clusterDf.to_csv(self.resultDataDir + 'clusterRes.csv', index=False)
        print('cluster finish')

    def getStay(self):
        cluster_res = pd.read_csv(self.resultDataDir + 'clusterRes.csv')
        stayDf = pd.DataFrame(columns=('imsi', 'newPlot', 'start', 'end'))
        # 按id划分用户
        listType = self.listType
        userNum = self.userNum
        for i in range(0, userNum):
            tempUser = cluster_res[cluster_res['imsi'].isin([listType[i]])]
            userID = tempUser.iloc[0, 0]
            clusterType = tempUser['cluster'].unique()
            clusterNum = clusterType.size

            for j in range(0, clusterNum):

                tempCluster = tempUser[tempUser['cluster'].isin([clusterType[j]])]
                clusterID = tempCluster.iloc[0, 5]

                # 驻留点
                if (clusterID != -1):
                    start = tempCluster['date_time'].min()
                    end = tempCluster['date_time'].max()
                    lat = round(tempCluster['latitude'].mean(), 8)
                    lon = round(tempCluster['longitude'].mean(), 8)

                    # plot=round(tempCluster['newPlot'].mode()[0],0)
                    # plot修改为lat和lon的nearest plot
                    plot = findPlot(lat, lon, self.station)

                    stay_tmp = pd.DataFrame([userID, plot, start, end]).T
                    stay_tmp.columns = stayDf.columns

                    # 把两个dataframe合并，需要设置 ignore_index=True
                    stayDf = pd.concat([stayDf, stay_tmp], ignore_index=True)

        # 以人为单位，按出发时间排序
        stayDf = stayDf.sort_values(['imsi', 'start'])
        stayDf.to_csv(self.resultDataDir + 'stayPoint.csv', index=False)
        print('stay finish')

    def getTrip(self):
        cluster_res = pd.read_csv(self.resultDataDir + 'clusterRes.csv')
        cluster_res = cluster_res.drop(['longitude', 'latitude'], axis=1)
        tempRes = pd.DataFrame(columns=('imsi', 'start', 'end', 'startPlot', 'endPlot','cluster'))
        # 按id划分用户
        listType = self.listType
        userNum = self.userNum
        for i in range(0, userNum):
            tempUser = cluster_res[cluster_res['imsi'].isin([listType[i]])]
            userID = tempUser.iloc[0, 0]
            clusterType = tempUser['cluster'].unique()
            clusterNum = clusterType.size

            for j in range(0, clusterNum):

                tempCluster = tempUser[tempUser['cluster'].isin([clusterType[j]])]
                clusterID = tempCluster.iloc[0, 3]

                # 驻留类化简
                if (clusterID != -1):
                    start = tempCluster['date_time'].min()
                    end = tempCluster['date_time'].max()

                    startPlot = tempCluster.iloc[0, 1]
                    endPlot = tempCluster.iloc[tempCluster.shape[0] - 1, 1]
                    temp = pd.DataFrame([userID, start, end, startPlot, endPlot,clusterID]).T
                    # 修改当前数据的column一致
                    temp.columns = tempRes.columns
                    # 把两个dataframe合并，需要设置 ignore_index=True
                    tempRes = pd.concat([tempRes, temp], ignore_index=True)

                # 出行点
                else:
                    tempCluster['start'] = tempCluster['date_time']
                    tempCluster['end'] = tempCluster['date_time']
                    tempCluster['startPlot'] = tempCluster['newPlot']
                    tempCluster['endPlot'] = tempCluster['newPlot']
                    temp = tempCluster['cluster'].copy()
                    tempCluster.drop(['cluster'], inplace=True, axis=1)
                    tempCluster.drop(['date_time'], inplace=True, axis=1)
                    tempCluster.drop(['newPlot'], inplace=True, axis=1)
                    tempCluster['cluster']=temp
                    tempRes = pd.concat([tempRes, tempCluster], ignore_index=True)

        # 以人为单位，按出发时间排序
        tempRes = tempRes.sort_values(['imsi', 'start'])
        travelPath = pd.DataFrame(columns=('imsi', 'start', 'end', 'startPlot', 'endPlot'))

        for i in range(0, userNum):
            tempUser = tempRes[tempRes['imsi'].isin([listType[i]])]
            userID = tempUser.iloc[0, 0]
            entryNum = tempUser.shape[0]
            for j in range(0, entryNum - 1):
                start = tempUser.iloc[j, 1]
                end = tempUser.iloc[j + 1, 2]

                if end - start > 2 * 60 * 60 * 1000:
                    continue
                startPlot = tempUser.iloc[j, 4]
                endPlot = tempUser.iloc[j + 1, 3]
                if startPlot==endPlot:
                    continue
                travel_tmp = pd.DataFrame([userID, start, end, startPlot, endPlot]).T
                # 修改当前数据的column一致
                travel_tmp.columns = travelPath.columns
                travelPath = pd.concat([travelPath, travel_tmp], ignore_index=True)
        travelPath.to_csv(self.resultDataDir + 'travelPath.csv', index=False)
        print('travel finish')

    def aggregateStay(self, slot=5):
        """
        驻留数据分箱
        :param slot:
        :return:
        """
        df = pd.read_csv(self.resultDataDir + 'stayPoint.csv')
        df['start'] -= 1538496000000
        df['start'] /= 1000
        df['start'] /= 60 * slot
        df['start'] = df['start'].astype(int)
        df['end'] -= 1538496000000
        df['end'] /= 1000
        df['end'] /= 60 * slot
        df['end'] = df['end'].astype(int)
        json = [{} for i in range(288)]
        for name, gp in df.groupby(['newPlot', 'start', 'end']):
            plot, start, end = name
            for i in range(start, end + 1):
                plot = self.station2box[str(plot)]
                if json[i].__contains__(plot):
                    json[i][plot] += len(gp)
                else:
                    json[i][plot] = len(gp)
        self.saveJson(json, self.finalDir + 'spaceStayDataset.json')
        return json

    def aggregateTrip(self, slot=5):
        """
        出行轨迹分箱，共计9846人次出行
        :param slot:
        :return:
        """
        df = pd.read_csv(self.resultDataDir + 'travelPath.csv')
        df['start'] -= 1538496000000
        df['start'] /= 1000
        df['start'] /= 60 * slot
        df['start'] = df['start'].astype(int)
        df['end'] -= 1538496000000
        df['end'] /= 1000
        df['end'] /= 60 * slot
        df['end'] = df['end'].astype(int)
        json = [{} for i in range(288)]
        record={}
        for name, gp in df.groupby(['start', 'end', 'startPlot', 'endPlot']):
            start, end, startPlot, endPlot = name

            startPlot = self.station2box[str(startPlot)]
            endPlot = self.station2box[str(endPlot)]
            for i in range(start, end + 1):
                if not json[i].__contains__(''+str(startPlot)+'-'+str(endPlot)):
                    json[i][''+str(startPlot)+'-'+str(endPlot)]={'source': str(startPlot), 'target': str(endPlot), 'weight': len(gp)}
                else:
                    json[i][''+str(startPlot)+'-'+str(endPlot)]['weight']+=len(gp)
                    print(json[i][''+str(startPlot)+'-'+str(endPlot)]['weight'])

        temp = [[] for i in range(288)]
        for i in range(len(json)): # time
            for key in json[i].keys():
                temp[i].append(json[i][key])

        self.saveJson(temp, self.finalDir + 'spaceTripDataset.json')
