import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

travelPath="travelPath.csv"
clusterRes="clusterRes.csv"
tempRes="tempRes.csv"


def showEntry(fileName,sid,eid):
    print(fileName)
    df=pd.read_csv(fileName)

    listType = df['imsi'].unique()
    userNum=listType.size


    for i in range(userNum):
        tempUser=df[df['imsi'].isin([listType[i]])]
        entryNum=tempUser.shape[0]

        if eid==sid:
            tempUser['date_time']=pd.to_datetime(tempUser['date_time'] + 28800000, unit='ms')

        else:
            tempUser['start'] = pd.to_datetime(tempUser['start'] + 28800000, unit='ms')
            tempUser['end'] = pd.to_datetime(tempUser['end'] + 28800000, unit='ms')


        for j in range(0,entryNum):
            start=tempUser.iloc[j, sid]
            if(sid==eid):
                end=tempUser.iloc[j,sid+1]
            else:
                end = tempUser.iloc[j, eid]
            print([start,end])
    print("______________________________________________________________________________________")
#
# showEntry(clusterRes,4,4)
#
# showEntry(tempRes,3,4)

showEntry(travelPath,1,2)

