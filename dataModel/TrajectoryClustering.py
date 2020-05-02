import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.STDBSCAN import *

import time
import warnings

warnings.filterwarnings('ignore')



def isOutlier(travelTime):
    res = stayRange[(stayRange['start'] < travelTime['date_time']) & (stayRange['end'] > travelTime['date_time'])]
    if(res.size!=0):
        print(userID)
        return False
    return True


def plotFeature(df_clustering):
    data=df_clustering[['longitude', 'latitude']].values
    labels_=df_clustering.iloc[:,5].values
    clusterNum=len(set(labels_))
    fig = plt.figure()
    scatterColors = ['black', 'blue', 'green', 'yellow', 'red', 'purple', 'orange','#BC8F8F','#8B4513','brown']
    ax = fig.add_subplot(111)
    for i in range(-1,clusterNum):
        colorSytle = scatterColors[i % len(scatterColors)]
        subCluster = data[np.where(labels_==i)]
        ax.scatter(subCluster[:,0], subCluster[:,1], c=colorSytle, s=20)
    plt.show()

def findPlot(lat, lon, station):
    station['x'] = lat - station['latitude']
    station['y'] = lon - station['longitude']
    station['dist'] = station['x'] ** 2 + station['y'] ** 2
    id = station['dist'].idxmin()

    return id

def getDist(lat1,lon1,lat2,lon2):
    distance = great_circle((lat1, lon1), (lat2, lon2)).meters
    return distance

# 读取数据
df=pd.read_csv('../resultData/dataAfterWash.csv')
station=pd.read_csv('../finalData/newStation.csv')

# 调整时间格式
df['date_time']=df['timestamp']
# df['date_time']=pd.to_datetime(df['timestamp']+28800000,unit='ms')
df.drop(['timestamp'], inplace=True, axis=1)


# TODO 调参
# STDBSCAN参数
spatial_threshold = 1500 # meters
temporal_threshold = 200  # minutes
min_neighbors = 1

# 按id划分用户
listType = df['imsi'].unique()
userNum=listType.size

start = time.clock()

# 聚类结果
cluster_res=pd.DataFrame(columns=['imsi', 'longitude', 'latitude','newPlot','date_time','cluster'])

for i in range(0,userNum):
    tempUser=df[df['imsi'].isin([listType[i]])]
    # 对每个用户的数据进行聚类
    df_clustering = ST_DBSCAN(tempUser, spatial_threshold, temporal_threshold, min_neighbors)
    cluster_res = cluster_res.append(df_clustering)
    # 可视化
    # plotFeature(df_clustering)

# 聚类操作的时间
end = time.clock()
print('cluster finish all in %s s' % str(end - start))


#
cluster_res.to_csv('../resultData/clusterRes.csv', index=False)

# cluster_res=pd.read_csv('../resultData/clusterRes.csv')


# # 将pandas.timestamp还原成原始的unix时间戳
# cluster_res['timestamp']=[t.value/1000000-28800000 for t in cluster_res.date_time]
# cluster_res.drop(['date_time'], inplace=True, axis=1)

# 驻留点
stayPoint=pd.DataFrame(columns=('imsi','longitude','latitude','newPlot','start','end'))
# 出行路径

# 修改：加入时间距离速度三个属性
travelPath=pd.DataFrame(columns=('imsi', 'start', 'end','startPlot','endPlot','usedTime','distance','speed'))

tempRes=pd.DataFrame(columns=('imsi','longitude','latitude','start','end','startPlot','endPlot'))




"""""
处理聚类结果


1.stayPoint:
    将每一类的数据计算成一条新的数据（类别不为-1）
    imsi-longitude-latitude-newPlot-start-end
    
    
1.5 将某一类中间出现的clusterID为-1的点删除


2.tempRes:
    将stayPoint中数据的newPlot属性改为startPlot和endPlot
    对于类别为-1的将date_time和newPlot属性都扩充成start(Plot)&end(Plot)，直接拼接
    将上述结果以人为单位，按照start进行排序

3.travelPath:
    遍历tempRes将每一条的start(Plot)和下一条的end(Plot)形成一条新的数据

"""""
stayRange=pd.DataFrame(columns=( 'start', 'end'))
for i in range(0,userNum):
    tempUser = cluster_res[cluster_res['imsi'].isin([listType[i]])]
    userID=listType[i]
    # print("__________________________________")
    # print(userID)

    clusterType=tempUser['cluster'].unique()
    clusterNum=clusterType.size
    clusterType=np.sort(clusterType)

    if(clusterType.size==1):
        print(clusterType,userID)

    stayRange=pd.DataFrame(columns=( 'start', 'end'))

    # 驻留点
    for j in range(1,clusterNum):

        tempCluster=tempUser[tempUser['cluster'].isin([clusterType[j]])]
        clusterID=tempCluster.iloc[0,5]

        if(clusterID!=-1):
            start=tempCluster['date_time'].min()
            end=tempCluster['date_time'].max()
            lat=round(tempCluster['latitude'].mean(),8)
            lon=round(tempCluster['longitude'].mean(),8)

            # plot=round(tempCluster['newPlot'].mode()[0],0)
            # plot修改为lat和lon的nearest plot
            plot=findPlot(lat,lon,station)

            startPlot=tempCluster.iloc[0, 3]
            endPlot=tempCluster.iloc[tempCluster.shape[0]-1, 3]

            stay_tmp = pd.DataFrame([userID,lon,lat,plot,start,end]).T
            # 修改：不这么写的话 由于类型问题 会导致imsi出错
            stay_tmp[0]=stay_tmp[0].astype(int)
            stay_tmp[0]=userID

            temp=pd.DataFrame([userID,lon,lat,start,end,startPlot,endPlot]).T
            # 修改：不这么写的话 由于类型问题 会导致imsi出错
            stay_tmp[0] = stay_tmp[0].astype(int)
            temp[0]=temp[0].astype(int)
            temp[0]=userID
            # 修改当前数据的column一致
            stay_tmp.columns = stayPoint.columns
            temp.columns = tempRes.columns

            temp['imsi']=int(temp['imsi'])
            # 把两个dataframe合并，需要设置 ignore_index=True
            stayPoint = pd.concat([stayPoint, stay_tmp], ignore_index=True)
            tempRes = pd.concat([tempRes, temp], ignore_index=True)

            range22=pd.DataFrame([start,end]).T
            range22.columns=stayRange.columns
            stayRange=pd.concat([stayRange, range22], ignore_index=True)

        # 出行点
        # else:
        #     tempCluster['start']=tempCluster['date_time']
        #     tempCluster['end'] = tempCluster['date_time']
        #     tempCluster['startPlot']=tempCluster['newPlot']
        #     tempCluster['endPlot']=tempCluster['newPlot']
        #     tempCluster.drop(['cluster'], inplace=True, axis=1)
        #     tempCluster.drop(['date_time'], inplace=True, axis=1)
        #     tempCluster.drop(['newPlot'], inplace=True, axis=1)
        #
        #
        #     tempRes = pd.concat([tempRes, tempCluster], ignore_index=True)


    # 出行点
    tempCluster = tempUser[tempUser['cluster'].isin([clusterType[0]])]

    clusterID = tempCluster.iloc[0, 5]
    tempCluster = tempCluster[tempCluster.apply(isOutlier, axis=1) == True]

    tempCluster['start']=tempCluster['date_time']
    tempCluster['end'] = tempCluster['date_time']
    tempCluster['startPlot']=tempCluster['newPlot']
    tempCluster['endPlot']=tempCluster['newPlot']
    tempCluster.drop(['cluster'], inplace=True, axis=1)
    tempCluster.drop(['date_time'], inplace=True, axis=1)
    tempCluster.drop(['newPlot'], inplace=True, axis=1)

    tempRes = pd.concat([tempRes, tempCluster], ignore_index=True)


tempRes["imsi"] = tempRes["imsi"].astype("int")
tempRes=tempRes.sort_values(['imsi','start'])
tempRes.to_csv('../resultData/tempRes.csv', index=False)

# 以人为单位，按出发时间排序
stayPoint=stayPoint.sort_values(['imsi','start'])
# tempRes=tempRes.sort_values(['imsi','start'])

print(userNum)
listType = tempRes['imsi'].unique()
userNum=listType.size
print(userNum)
# 形成出行数据
for i in range(0,userNum):
    tempUser = tempRes[tempRes['imsi'].isin([listType[i]])]

    userID = tempUser.iloc[0, 0]
    entryNum=tempUser.shape[0]
    for j in range(0,entryNum-1):

        start=tempUser.iloc[j, 4]
        end=tempUser.iloc[j+1, 3]
        startPlot=tempUser.iloc[j, 6]
        endPlot=tempUser.iloc[j+1, 5]
        # 分钟，千米，千米/时
        usedTime=(end-start)/1000/60
        distance=getDist(tempUser.iloc[j,2],tempUser.iloc[j,1],tempUser.iloc[j+1,2],tempUser.iloc[j+1,1])/1000
        speed=distance/(usedTime/60)

        travel_tmp = pd.DataFrame([userID, start, end, startPlot, endPlot,usedTime,distance,speed]).T
        # 修改当前数据的column一致
        travel_tmp.columns = travelPath.columns
        travelPath = pd.concat([travelPath, travel_tmp], ignore_index=True)

# 去除startPlot==endPlot,distance=0的情况
travelPath=travelPath[travelPath['startPlot']!=travelPath['endPlot']]

stayPoint.to_csv('../resultData/stayPoint.csv', index=False)
travelPath.to_csv('../resultData/travelPath.csv', index=False)









