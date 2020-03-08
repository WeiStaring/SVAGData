from dataModel.BaseModel import *


class SpaceFlowModel(BaseModel):
    def __init__(self):
        super().__init__()

    def dataPipeline(self):
        df = pd.read_csv(self.dataDir + 'dataAfterWash.csv')
        df = self.records2Slot(df)
        mat = self.SlotRecords2Matrix(df)

    def records2Slot(self, df, slot=5):
        """
        将记录划分到槽，并去重
        :param slot: 槽大小
        :return: df
        """
        df['timestamp'] -= 1538496000000
        df['timestamp'] /= 1000
        # 使用5分钟作为时间槽 9849->8179
        df['timestamp'] /= 60 * slot
        df['timestamp'] = df['timestamp'].astype(int)
        df = df.drop_duplicates(['timestamp', 'laci', 'imsi'])
        return df

    def SlotRecords2Matrix(self, df):
        mat = np.zeros((288, 2793),dtype='int16')
        for name, gp in df.groupby(['timestamp', 'laci']):
            time, plot = name
            mat[int(time),int(plot)]=len(gp)
        print(np.sum(mat))
        return mat
