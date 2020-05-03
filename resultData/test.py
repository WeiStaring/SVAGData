import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from geopy.distance import great_circle

warnings.filterwarnings('ignore')

def showTempRes():
    fileName="tempRes.csv"
    df=pd.read_csv(fileName)

    listType = df['imsi'].unique()
    userNum=listType.size


    print(fileName)


    for i in range(0,2):
        print("用户",i)
        tempUser=df[df['imsi'].isin([listType[i]])]
        entryNum=tempUser.shape[0]


        tempUser['start'] = pd.to_datetime(tempUser['start'] + 28800000, unit='ms')
        tempUser['end'] = pd.to_datetime(tempUser['end'] + 28800000, unit='ms')


        for j in range(0,entryNum):
            start=tempUser.iloc[j, 3]

            end = tempUser.iloc[j, 4]

            startPlot=tempUser.iloc[j,5]

            endPlot = tempUser.iloc[j, 6]

            print([start,end,startPlot,endPlot])
    print("______________________________________________________________________________________")


def showClusterRes():
    fileName="clusterRes.csv"
    df=pd.read_csv(fileName)

    listType = df['imsi'].unique()
    userNum=listType.size

    print(fileName)

    for i in range(12,13):
        print("用户", i)
        tempUser=df[df['imsi'].isin([listType[i]])]
        entryNum=tempUser.shape[0]

        tempUser['date_time']=pd.to_datetime(tempUser['date_time'] + 28800000, unit='ms')


        for j in range(0,entryNum):
            start=tempUser.iloc[j, 4]
            plot=tempUser.iloc[j,3]
            clusterID=tempUser.iloc[j,5]

            print([start,plot,clusterID])
    print("______________________________________________________________________________________")


def showTravelPath():
    fileName="travelPath.csv"
    df = pd.read_csv(fileName)

    listType = df['imsi'].unique()
    userNum = listType.size

    print(fileName)
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(0,userNum):

        # print("用户",i)
        tempUser = df[df['imsi'].isin([listType[i]])]
        entryNum = tempUser.shape[0]


        tempUser['start'] = pd.to_datetime(tempUser['start'] + 28800000, unit='ms')
        tempUser['end'] = pd.to_datetime(tempUser['end'] + 28800000, unit='ms')

        for j in range(0, entryNum):
            start = tempUser.iloc[j, 1]
            end = tempUser.iloc[j, 2]

            startPlot=tempUser.iloc[j, 3]
            endPlot=tempUser.iloc[j,4]
            # print([start, end, startPlot, endPlot])
            distance=tempUser.iloc[j,6]

            # 出行时间为负数

            if(start>end):
                print([i,start, end, startPlot, endPlot,distance])

            # 出行距离为0
            if(startPlot==endPlot):
                continue
            # print([i,start, end, startPlot, endPlot,distance])
            if(startPlot==endPlot and distance==0):
                count2+=1
            if(startPlot==endPlot and distance!=0):
                count3+=1


    print(count1,count2,count3)



    print("______________________________________________________________________________________")

# showClusterRes()
# showTempRes()
showTravelPath()

def getDist(lat1,lon1,lat2,lon2):
    distance = great_circle((lat1, lon1), (lat2, lon2)).meters
    return distance
