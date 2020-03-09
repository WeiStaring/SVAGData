import pandas as pd
import numpy as np
import json

class BaseModel:
    def __init__(self):
        self.dataDir = 'data/'
        self.resultDataDir = 'resultData/'
        self.imagesDir = 'imagesDir/'

    def saveJson(self,file,filename):
        with open(self.resultDataDir+filename, 'w') as file_obj:
            json.dump(file, file_obj)
        print('saveJson accomplished')


class WashDataModel(BaseModel):
    def __init__(self):
        super().__init__()

    def washData(self):
        df = pd.read_csv(self.dataDir+'data.csv')
        station = pd.read_csv(self.dataDir+'station.csv')
        station['plot']=station.index
        print(df.info())
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

        # 去除干扰数据条目（不是2018.10.03当天的数据）10137条->7452条
        df_test = df_new[1538496000000<=df_new['timestamp']]
        df_test = df_test[df_test['timestamp']<1538582400000]

        # 去除两数据源关联后经纬度为空的数据条目
        df_test['laci'] = df_test['lac_id'].str.cat(df_test['cell_id'], sep='-')
        df_test = df_test[df_test['laci'].isin(station['laci'])]
        df_res = pd.merge(df_test, station)

        # 剔除经纬度在第一个参数里加入‘longtidue’和‘latitude’
        df_res.drop(["lac_id","cell_id",'laci'], inplace=True, axis=1)
        station.drop(['laci'],inplace=True,axis=1)

        # 以人为单位，按时间正序排序
        df_res = df_res.sort_values(['imsi','timestamp'])
        # 输出csv
        print(df_res.info())

        df_res.to_csv(self.dataDir+'dataAfterWash.csv', index=False)
        station.to_csv(self.resultDataDir+'newStation.csv',index=False)

