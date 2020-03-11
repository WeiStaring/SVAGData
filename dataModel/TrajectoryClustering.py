import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.STDBSCAN import *
import time


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


#读取数据
df=pd.read_csv('../data/dataAfterWash.csv')

#调整时间格式
df['date_time']=pd.to_datetime(df['timestamp']+28800000,unit='ms')
df.drop(['timestamp'], inplace=True, axis=1)



#TODO 调参
#STDBSCAN参数
spatial_threshold = 1000 # meters
temporal_threshold = 30  # minutes
min_neighbors = 3

#按id划分用户
listType = df['imsi'].unique()
userNum=listType.size



start = time.clock()


for i in range(0,userNum):
    tempUser=df[df['imsi'].isin([listType[i]])]
    # 聚类
    df_clustering = ST_DBSCAN(tempUser, spatial_threshold, temporal_threshold, min_neighbors)


    #TODO 处理聚类结果



    # # 可视化
    plotFeature(df_clustering)

#聚类操作的时间
end = time.clock()
print('finish all in %s s' % str(end - start))



