import pandas as pd
import numpy as np
import warnings
import json

warnings.filterwarnings('ignore')
# 设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
f = open("../finalData/station2box.json", encoding='utf-8')
station2box= json.load(f)
stayPoint=pd.read_csv("../resultData/stayPoint.csv")
station=pd.read_csv('../finalData/newStation.csv')

# 使用工作、居住停留点的时间分布特征对stayPoint类型进行判断
# 居住时段 0：00-7：00 20：00-0：00
# 工作时段 9：00-12：00 14：00-17：00

time0=pd.Timestamp(2018,10,3,0)
time7=pd.Timestamp(2018,10,3,7)
time9=pd.Timestamp(2018,10,3,9)
time12=pd.Timestamp(2018,10,3,12)
time14=pd.Timestamp(2018,10,3,14)
time17=pd.Timestamp(2018,10,3,17)
time20=pd.Timestamp(2018,10,3,20)
time24=pd.Timestamp(2018,10,4,0)

def getType(x):
    if (x['homeCount'] > x['workCount']):
        return "home"
    if (x['homeCount'] < x['workCount']):
        return "work"

    return "home&work"

def findPlot(lat, lon, station):
    station['x'] = lat - station['latitude']
    station['y'] = lon - station['longitude']
    station['dist'] = station['x'] ** 2 + station['y'] ** 2
    id = station['dist'].idxmin()
    return id

def isHome(x):
    morning=x['start']>time0 and x['end']<time7
    evening=x['start']>time20 and x['end']<time24
    return morning or evening

def isWork(x):
    morning = x['start']> time9 and x['end'] < time12
    evening =x['start'] > time14 and x['end']< time17
    return morning or evening


# step1:将停留点按时间顺序排列

stayPoint.sort_values(['imsi','start'])

# step2:遍历停留点，将停留时间小于15min的剔除
# 剔除包含轨迹点数少于10个的？一条停留数据包含的轨迹点数在当前数据中未保留
stayPoint['stayTime']=(stayPoint['end']-stayPoint['start'])/1000/60

validStay=stayPoint[stayPoint['stayTime']>15]
validStay['start']=pd.to_datetime(validStay['start']+28800000,unit='ms')
validStay['end']=pd.to_datetime(validStay['end']+28800000,unit='ms')


# step3:遍历剩余停留点，筛选出起止时间均位于居住时段的停留点，将其加入候选居住停留点集合

validStay['home']=validStay.apply(isHome,axis=1)
validStay['work']=validStay.apply(isWork,axis=1)

candidateHome=validStay[validStay['home']]
candidateWork=validStay[validStay['work']]
# validStay.to_csv("../resultData/validStay.csv")



# step4:遍历候选居住停留点集合，根据每个停留点包含的轨迹点数占总轨迹点数比重进行加权平均得到居住点经纬度
# 包含轨迹点数问题


home=pd.DataFrame(columns=('imsi','longitude','latitude','plot','box'))
work=pd.DataFrame(columns=('imsi','longitude','latitude','plot','box'))



listType = candidateHome['imsi'].unique()
userNum=listType.size

for i in range(0,userNum):
    tempUser=candidateHome[candidateHome['imsi'].isin([listType[i]])]
    lon=tempUser['longitude'].mean()
    lat=tempUser['latitude'].mean()
    plot = findPlot(lat, lon, station)
    box = station2box[str(plot)]
    userID = listType[i]
    temp = pd.DataFrame([userID, lon, lat,plot,box]).T

    # 修改：不这么写的话 由于类型问题 会导致imsi出错
    temp[0] = temp[0].astype(int)
    temp[0] = userID
    temp[3] = temp[3].astype(int)
    temp[4] = temp[4].astype(int)
    # 修改当前数据的column一致
    temp.columns = home.columns
    # 把两个dataframe合并，需要设置 ignore_index=True
    home = pd.concat([home, temp], ignore_index=True)


listType = candidateWork['imsi'].unique()
userNum=listType.size

for i in range(0, userNum):
    tempUser = candidateWork[candidateWork['imsi'].isin([listType[i]])]
    lon = tempUser['longitude'].mean()
    lat = tempUser['latitude'].mean()
    plot = findPlot(lat, lon, station)
    box = station2box[str(plot)]
    userID = listType[i]
    temp = pd.DataFrame([userID, lon, lat,plot,box]).T

    # 修改：不这么写的话 由于类型问题 会导致imsi出错
    temp[0] = temp[0].astype(int)
    temp[0] = userID
    temp[3] = temp[3].astype(int)
    temp[4] = temp[4].astype(int)
    # 修改当前数据的column一致
    temp.columns = work.columns
    # 把两个dataframe合并，需要设置 ignore_index=True
    work = pd.concat([work,temp], ignore_index=True)



homeCounts=home['box'].value_counts()
tempDict= {'box':homeCounts.index,'homeCount':homeCounts.values}
df_home = pd.DataFrame(tempDict)
df_home=df_home.sort_values(['box'])
df_home.reset_index(drop=True, inplace=True)


workCounts=work['box'].value_counts()
tempDict= {'box':workCounts.index,'workCount':workCounts.values}
df_work = pd.DataFrame(tempDict)
df_work=df_work.sort_values(['box'])
df_work.reset_index(drop=True, inplace=True)



df=pd.merge(df_home,df_work,how='outer')
df=df.sort_values(['box'])
df.reset_index(drop=True, inplace=True)
df=df.where(df.notnull(), 0)
df['type']=df.apply(getType,axis=1)
print(df)



df.to_csv("../resultData/boxType.csv")


