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

cluster_res=pd.DataFrame(columns=['imsi', 'longitude', 'latitude','plot','date_time','cluster'])

for i in range(0,userNum):
    tempUser=df[df['imsi'].isin([listType[i]])]
    # 聚类
    df_clustering = ST_DBSCAN(tempUser, spatial_threshold, temporal_threshold, min_neighbors)
    cluster_res = cluster_res.append(df_clustering)
    # # 可视化
    # plotFeature(df_clustering)

# 聚类操作的时间
end = time.clock()
print('finish all in %s s' % str(end - start))

# # 将pandas.timestamp还原成原始的unix时间戳
# cluster_res['timestamp']=[t.value/1000000-28800000 for t in cluster_res.date_time]
# cluster_res.drop(['date_time'], inplace=True, axis=1)


stayPoint=pd.DataFrame(columns=('imsi','longitude','latitude','plot','start','end'))
travelPoint=pd.DataFrame(columns=('imsi', 'longitude', 'latitude','plot','date_time'))


for i in range(0,userNum):
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
            plot=round(tempCluster['plot'].mode()[0],0)

            stay_tmp = pd.DataFrame([userID,lon,lat,plot,start,end]).T
            # 修改当前数据的column一致
            stay_tmp.columns = stayPoint.columns
            # 把两个dataframe合并，需要设置 ignore_index=True
            stayPoint = pd.concat([stayPoint, stay_tmp], ignore_index=True)

        # 出行点
        else:
            tempCluster.drop(['cluster'], inplace=True, axis=1)

            travelPoint = pd.concat([travelPoint, tempCluster], ignore_index=True)



# print(cluster_res.info())
# print(travelPoint.info())
# print(stayPoint.info())

# 以人为单位，按时间正序排序
cluster_res = cluster_res.sort_values(['imsi', 'date_time'])
travelPoint=travelPoint.sort_values(['imsi','date_time'])
stayPoint=stayPoint.sort_values(['imsi','start'])


# 输出csv
cluster_res.to_csv('../data/clusterResult.csv', index=False)
travelPoint.to_csv('../data/travelPoint.csv', index=False)
stayPoint.to_csv('../data/stayPoint.csv', index=False)





