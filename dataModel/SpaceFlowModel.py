from dataModel.BaseModel import *


class SpaceFlowModel(BaseModel):
    def __init__(self):
        super().__init__()

    def dataPipeline(self):
        df = pd.read_csv(self.dataDir + 'dataAfterWash.csv')
        df = self.records2Slot(df)
        json = self.SlotRecords2Matrix(df)
        self.saveJson(json,'spaceFlowDataset.json')

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
        df = df.drop_duplicates(['timestamp', 'plot', 'imsi'])
        return df

    def SlotRecords2Matrix(self, df):
        json = [{} for i in range(288)]
        for name, gp in df.groupby(['timestamp', 'plot']):
            time, plot = name
            json[int(time)][int(plot)] = len(gp)
        return json
