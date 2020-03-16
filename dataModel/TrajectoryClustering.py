import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataModel.STDBSCAN import *
import time
import warnings

warnings.filterwarnings('ignore')

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

# 读取数据
df=pd.read_csv('../data/dataAfterWash.csv')

# 调整时间格式
df['date_time']=pd.to_datetime(df['timestamp']+28800000,unit='ms')
df.drop(['timestamp'], inplace=True, axis=1)


# TODO 调参
# STDBSCAN参数
spatial_threshold = 1000 # meters
temporal_threshold = 30  # minutes
min_neighbors = 3

# 按id划分用户
listType = df['imsi'].unique()
userNum=listType.size


start = time.clock()

cluster_res=pd.DataFrame(columns=['imsi', 'longitude', 'latitude','newPlot','date_time','cluster'])

for i in range(0,2):
    tempUser=df[df['imsi'].isin([listType[i]])]
    # 聚类
    df_clustering = ST_DBSCAN(tempUser, spatial_threshold, temporal_threshold, min_neighbors)
    cluster_res = cluster_res.append(df_clustering)
    # 可视化
    # plotFeature(df_clustering)

# 聚类操作的时间
end = time.clock()
print('finish all in %s s' % str(end - start))

# # 将pandas.timestamp还原成原始的unix时间戳
# cluster_res['timestamp']=[t.value/1000000-28800000 for t in cluster_res.date_time]
# cluster_res.drop(['date_time'], inplace=True, axis=1)


stayPoint=pd.DataFrame(columns=('imsi','longitude','latitude','newPlot','start','end'))
travelPath=pd.DataFrame(columns=('imsi', 'start', 'end','startPlot','endPlot'))

tempRes=pd.DataFrame(columns=('imsi','longitude','latitude','newPlot','start','end'))


"""""
处理聚类结果

1.stayPoint:
    将每一类的数据计算成一条新的数据（类别不为-1）
    imsi-longitude-latitude-plot-start-end

2.tempRes:
    对于类别为-1的不需要计算，直接拼接
    将上述结果以人为单位，按照start进行排序

3.travelPath:
    遍历tempRes将每一条的start和下一条的end形成一条新的数据

"""""

for i in range(0,2):
    tempUser = cluster_res[cluster_res['imsi'].isin([listType[i]])]
    userID=tempUser.iloc[0,0]

    clusterType=tempUser['cluster'].unique()
    clusterNum=clusterType.size


    for j in range(0,clusterNum):

        tempCluster=tempUser[tempUser['cluster'].isin([clusterType[j]])]
        clusterID=tempCluster.iloc[0,5]

        # 驻留点
        if(clusterID!=-1):
            start=tempCluster['date_time'].min()
            end=tempCluster['date_time'].max()
            lat=round(tempCluster['latitude'].mean(),8)
            lon=round(tempCluster['longitude'].mean(),8)
            plot=round(tempCluster['newPlot'].mode()[0],0)

            stay_tmp = pd.DataFrame([userID,lon,lat,plot,start,end]).T
            # 修改当前数据的column一致
            stay_tmp.columns = stayPoint.columns
            # 把两个dataframe合并，需要设置 ignore_index=True
            stayPoint = pd.concat([stayPoint, stay_tmp], ignore_index=True)
            tempRes = pd.concat([tempRes, stay_tmp], ignore_index=True)

        # 出行点
        else:
            tempCluster['start']=tempCluster['date_time']
            tempCluster['end'] = tempCluster['date_time']
            tempCluster.drop(['cluster'], inplace=True, axis=1)
            tempCluster.drop(['date_time'], inplace=True, axis=1)

            tempRes = pd.concat([tempRes, tempCluster], ignore_index=True)

stayPoint=stayPoint.sort_values(['imsi','start'])
tempRes=tempRes.sort_values(['imsi','start'])

for i in range(0,2):
    tempUser = tempRes[tempRes['imsi'].isin([listType[i]])]
    userID = tempUser.iloc[0, 0]
    entryNum=tempUser.shape[0]
    for j in range(0,entryNum-1):
        start=tempUser.iloc[j, 5]
        end=tempUser.iloc[j+1, 4]
        startPlot=tempUser.iloc[j, 3]
        endPlot=tempUser.iloc[j+1, 3]

        travel_tmp = pd.DataFrame([userID, start, end, startPlot, endPlot]).T
        # 修改当前数据的column一致
        travel_tmp.columns = travelPath.columns

        travelPath = pd.concat([travelPath, travel_tmp], ignore_index=True)


cluster_res.to_csv('../resultData/clusterRes.csv', index=False)
stayPoint.to_csv('../resultData/stayPoint.csv', index=False)
travelPath.to_csv('../resultData/travelPath.csv', index=False)


# tempRes.to_csv('../resultData/tempRes.csv', index=False)



