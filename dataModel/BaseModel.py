import pandas as pd
import numpy as np
import json

class BaseModel:
    def __init__(self):
        self.dataDir = 'data/'
        self.resultDataDir = 'resultData/'
        self.imagesDir = 'imagesDir/'
        self.finalDir = 'finalData/'

    def saveJson(self,file,path):
        with open(path, 'w') as file_obj:
            json.dump(file, file_obj)
        print('saveJson accomplished')

    def loadJson(self,path):
        f = open(path, encoding='utf-8')
        res = json.load(f)
        return res

class WashDataModel(BaseModel):
    def __init__(self):
        super().__init__()

    def washData(self):
        df = pd.read_csv(self.dataDir+'data.csv')
        # 为了精度，用str读取浮点数
        station = pd.read_csv(self.dataDir+'drop_duplicates_station.csv',dtype={'longitude': str, 'latitude': str})
        df.dropna(subset=['imsi', 'lac_id', 'cell_id'], inplace=True)
        #将基站id转成字符
        df['lac_id'] = df['lac_id'].astype(np.long).astype(str)
        df['cell_id'] = df['cell_id'].astype(np.long).astype(str)
        # 抽取timestamp,imsi,lac_id,cell_id 四个字段
        df.drop(['phone', 'timestamp1', 'tmp0', 'tmp0', 'tmp1', 'nid', 'npid'], inplace=True, axis=1)
        # 去除imsi中，包含特殊字符的数据条目（‘#’,’*’,’^’） 8条
        df['imsi'] = df['imsi'].astype(str)
        df = df[~df['imsi'].str.contains('\#')]
        df = df[~df['imsi'].str.contains('\^')]
        df_new = df[~df['imsi'].str.contains('\*')]

        df_test = df_new[1538496000000<=df_new['timestamp']]
        df_test = df_test[df_test['timestamp']<1538582400000]

        # 去除两数据源关联后经纬度为空的数据条目
        df_test['laci'] = df_test['lac_id'].str.cat(df_test['cell_id'], sep='-')
        df_test = df_test[df_test['laci'].isin(station['laci'])]
        df_res = pd.merge(df_test, station)

        # 剔除经纬度在第一个参数里加入‘longtidue’和‘latitude’
        df_res.drop(["lac_id","cell_id",'laci'], inplace=True, axis=1)
        station.drop(['laci'],inplace=True,axis=1)
        station = station.drop_duplicates(['newPlot'])
        # 以人为单位，按时间正序排序
        df_res = df_res.sort_values(['imsi','timestamp'])
        # 输出csv
        print(df_res.info())

        df_res.to_csv(self.resultDataDir+'dataAfterWash.csv', index=False)
        station.to_csv(self.finalDir+'newStation.csv',index=False)

    def station2box(self):
        json = self.loadJson(self.dataDir+"stationBoxes_204.json")
        station = pd.read_csv(self.finalDir+"newStation.csv")
        json = json['features']
        boxList=[]
        for item in json:
            coord = item['geometry']['coordinates']
            boxList.append([coord[0][0],coord[0][2]])
        dic={}
        for i in range(len(boxList)):
            c1,c2 = boxList[i]
            x1 = c1[0]
            x2 = c2[0]
            y1 = c1[1]
            y2 = c2[1]
            subStationDf = station[(x1<=station['longitude'])&(station['longitude']<=x2)]
            subStationDf = subStationDf[(y1<=subStationDf['latitude'])&(subStationDf['latitude']<=y2)]
            for j in range(len(subStationDf)):
                plot = subStationDf.iloc[j]['newPlot']
                if dic.__contains__(plot):
                    print('error')
                dic[int(plot)]=i
        self.saveJson(dic,self.finalDir+'station2box.json')




