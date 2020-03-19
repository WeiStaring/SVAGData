#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df=pd.read_csv('person1.csv')
df

#获取点坐标
x_values=[]
for item in df.iterrows():
    x_values.append(df.loc[item[0]]['startlatitude'])
    x_values.append(df.loc[item[0]]['endlatitude'])
print(x_values)

y_values=[]
for item in df.iterrows():
    y_values.append(df.loc[item[0]]['startlongitude'])
    y_values.append(df.loc[item[0]]['endlongitude'])
print(y_values)

z_values=[]
for item in df.iterrows():
    z_values.append(df.loc[item[0]]['type'])
    z_values.append(df.loc[item[0]]['type'])
print(z_values)

x_values=[122.8896332, 122.8960876, 122.8896332, 122.8741531, 122.8741531, 122.9067917, 122.9067917, 122.8947372, 122.8960876, 123.2350616, 123.2350616, 123.3034363, 123.3034363, 123.40065, 123.40065, 123.4119873]
y_values=[41.51470947, 41.51839828, 41.51470947, 41.50146866, 41.50146866, 41.52077866, 41.52077866, 41.51762009, 41.51839828, 41.76229858, 41.76229858, 41.77828979, 41.77828979, 41.79916, 41.79916, 41.8078804]
z_values=[3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]

x1=[122.8896332, 122.8960876, 122.8896332, 122.8741531, 122.8741531, 122.9067917, 122.9067917, 122.8947372, 122.8960876, 123.2350616]
y1=[41.51470947, 41.51839828, 41.51470947, 41.50146866, 41.50146866, 41.52077866, 41.52077866, 41.51762009, 41.51839828, 41.76229858]
x2=[123.2350616, 123.3034363, 123.3034363, 123.40065, 123.40065, 123.4119873]
y2=[41.76229858, 41.77828979, 41.77828979, 41.79916, 41.79916, 41.8078804]

#根据出行方式设置其颜色
plt.plot(x1,y1,c='r',label='3-riding')
plt.plot(x2,y2,c='y',label='4-transit')
#设置图表标题并给坐标轴加上标签
plt.title("Trip Mode(person1)",fontsize=14)
plt.xlabel("latitude",fontsize=14)
plt.ylabel("longitude",fontsize=14)

#设置刻度标记的大小
plt.tick_params(axis='both',which='major',labelsize=10)

plt.legend()
plt.show()

