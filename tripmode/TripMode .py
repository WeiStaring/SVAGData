#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8 -*-
from urllib.request import urlopen
import json
import hashlib
import requests

import pandas as pd
import numpy as np

np.set_printoptions(suppress=True)

#MyAK='jt2ebs4tgp1TyHowp3Ol4sOheMGH8S0u'
# MyAK='Pju1uy3aoutZxA16NX0xMgtwxX1xoqhs'
MySK=''


#调用百度API判断交通方式
def getduration(origin_path,result_path,MyAK,mytime):
    url_drive="http://api.map.baidu.com/directionlite/v1/driving?origin="+str(origin_path[0])+","+str(origin_path[1])+"&destination="+str(result_path[0])+","+str(result_path[1])+"&tactics=3&ak="+MyAK
    url_walk = "http://api.map.baidu.com/directionlite/v1/walking?origin="+str(origin_path[0])+","+str(origin_path[1])+"&destination="+str(result_path[0])+","+str(result_path[1])+"&tactics=3&ak="+MyAK
    url_ride="http://api.map.baidu.com/directionlite/v1/riding?origin="+str(origin_path[0])+","+str(origin_path[1])+"&destination="+str(result_path[0])+","+str(result_path[1])+"&tactics=3&ak="+MyAK
    url_bus="http://api.map.baidu.com/directionlite/v1/transit?origin="+str(origin_path[0])+","+str(origin_path[1])+"&destination="+str(result_path[0])+","+str(result_path[1])+"&tactics=3&ak="+MyAK
#     print(url_drive)
#     print(url_walk)    
#     print(url_ride)
#     print(url_bus)
    #从API读取驾驶数据
    response0 = requests.get(url_drive)
    answer0 = response0.json()
    if answer0['message']!="ok":
        answer[0]=float("inf")
    if len(answer0['result']['routes']) == 0:
        answer[0]=float("inf")
    else:
        answer[0]=answer0['result']['routes'][0]['duration']
    #从API读取步行数据
    response1 = requests.get(url_walk)
    answer1 = response1.json()
    if answer1['message']!="ok":
        answer[1]=float("inf")
    if len(answer1['result']['routes']) == 0:
        answer[1]=float("inf")
    else:
        answer[1]=answer1['result']['routes'][0]['duration']
    #从API读取骑行数据
    response2 = requests.get(url_ride)
    answer2 = response2.json()
    if answer2['message']!="ok":
        answer[2]=float("inf")
    if len(answer2['result']['routes']) == 0:
        answer[2]=float("inf")
    else:
        answer[2]=answer2['result']['routes'][0]['duration']
    #从API读取公交数据
    response3 = requests.get(url_bus)
    answer3 = response3.json()
    if answer3['message']!="ok":
        answer[3]=float("inf")
    else:
        answer[3]=answer3['result']['routes'][0]['duration']
    print(answer)
    print(mytime)
    
    y=0        
    x=float("inf")
    for i in answer:
        if abs(mytime-answer[i])<x:
            y=i+1
            x=abs(mytime-answer[i])
    print(y)
    return y

df_travel=pd.read_csv("travelPath.csv")
df_travel

#设置显示小数，转换换为时间戳格式
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
# startstamp = pd.to_datetime(df_travel['start'])
# df_travel['startstamp'] = (startstamp.values - np.datetime64('1970-01-01T08:00:00Z')) / np.timedelta64(1, 'ms')
# endstamp = pd.to_datetime(df_travel['end'])
# df_travel['endstamp'] = (endstamp.values - np.datetime64('1970-01-01T08:00:00Z')) / np.timedelta64(1, 'ms')
df_travel['mytime']=(df_travel['end']-df_travel['start'])/1000
df_travel

df_station=pd.read_csv("newStation.csv")
df_station

#获取起点坐标
def getstartpoint(origin_path,newPlot):
    origin_path[0]=df_station.loc[newPlot][1]
    origin_path[1]=df_station.loc[newPlot][0]
    return origin_path

#获取终点坐标
def getendpoint(result_path,newPlot):
    result_path[0]=df_station.loc[newPlot][1]
    result_path[1]=df_station.loc[newPlot][0]
    return result_path

#遍历获取出行方式
# origin_path=[0,0]
# result_path=[0,0]
# answer={0:0,1:0,2:0,3:0}
# getstartpoint(df_travel.loc[0][3])
# getendpoint(df_travel.loc[0][4])
# mytime=df_travel.loc[0][7]
# getduration(getstartpoint(df_travel.loc[0][3]),getendpoint(df_travel.loc[0][4]),MyAK,mytime)

for item in df_travel.iterrows():
    #遍历获取出行方式
    origin_path=[0,0]
    result_path=[0,0]
    answer={0:0,1:0,2:0,3:0}
    mytime=df_travel.loc[item[0]][5]
    origin_path=getstartpoint(origin_path,df_travel.loc[item[0]][3])
    result_path=getendpoint(result_path,df_travel.loc[item[0]][4])
    df_travel.loc[[item[0]],'startlatitude']=origin_path[1]
    df_travel.loc[[item[0]],'startlongitude']=origin_path[0]
    df_travel.loc[[item[0]],'endlatitude']=result_path[1]
    df_travel.loc[[item[0]],'endlongitude']=result_path[0]
    res=getduration(origin_path,result_path,MyAK,mytime)
    df_travel.loc[[item[0]],'type']=res

df_travel

df_1=df_travel
# del df_1['startstamp']
# del df_1['endstamp']
del df_1['mytime']
# df_1.to_csv('Result.csv')

df_1

df_1.to_csv( 'TripModeResult.csv',index=None)





