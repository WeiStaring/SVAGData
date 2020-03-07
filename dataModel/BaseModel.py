import pandas as pd
import numpy as np

class BaseModel:
    def __init__(self):
        self.dataDir = 'data/'
        self.resultDataDir = 'resultData/'
        self.imagesDir = 'imagesDir/'


class WashDataModel(BaseModel):
    def __init__(self):
        super().__init__()

    def washData(self):
        # 导入原始数据
        df = pd.read_csv(self.dataDir+'data.csv')
        # 导入基站坐标信息
        station = pd.read_csv(self.dataDir+'station.csv')

        # 去除空间信息残缺的记录条目（imsi、lac_id、cell_id中为空）
        df.dropna(subset=['imsi', 'lac_id', 'cell_id'], inplace=True)

        df['lac_id'] = df['lac_id'].astype(np.long).astype(str)
        df['cell_id'] = df['cell_id'].astype(np.long).astype(str)

        # 抽取timestamp,imsi,lac_id,cell_id 四个字段
        to_drop = ['phone', 'timestamp1', 'tmp0', 'tmp0', 'tmp1', 'nid', 'npid']
        df.drop(to_drop, inplace=True, axis=1)

        # 去除imsi中，包含特殊字符的数据条目（‘#’,’*’,’^’） 8条
        df['imsi'] = df['imsi'].astype(str)
        df = df[~df['imsi'].str.contains('\#')]
        df = df[~df['imsi'].str.contains('\^')]
        df_new = df[~df['imsi'].str.contains('\*')]

        # 去除干扰数据条目（不是2018.10.03当天的数据）10137条->7452条
        df_test = df_new[1538496000000<=df_new['timestamp']]
        df_test = df_test[df_test['timestamp']<1538582400000]
        print(df_test.info())
        print(np.max(df_test['timestamp']))
        print(np.min(df_test['timestamp']))
        # 去除两数据源关联后经纬度为空的数据条目 7452->7444
        df_test['laci'] = df_test['lac_id'].str.cat(df_test['cell_id'], sep='-')
        df_test = df_test[df_test['laci'].isin(station['laci'])]
        df_res = pd.merge(df_test, station)

        # 剔除经纬度在第一个参数里加入‘longtidue’和‘latitude’
        df_res.drop(["lac_id","cell_id"], inplace=True, axis=1)

        # TODO：
        # 以人为单位，按时间正序排序
        df_res = df_res.sort_values(['imsi','timestamp'])
        # 输出csv
        print(df_res.info())

        df_res.to_csv(self.resultDataDir+'dataAfterWash.csv', index=False)