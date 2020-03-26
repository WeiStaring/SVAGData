from dataModel.BaseModel import *


class SpaceVolumeModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.station2box = self.loadJson(self.finalDir+'station2box.json')

    def dataPipeline(self):
        df = pd.read_csv(self.resultDataDir + 'dataAfterWash.csv')
        df = self.records2Slot(df)
        self.station2box = self.loadJson(self.finalDir+'station2box.json')
        self.SlotRecords2Matrix(df)
        # self.getOdMatrix(df)

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
        df = df.drop_duplicates(['timestamp', 'newPlot', 'imsi'])
        return df

    def SlotRecords2Matrix(self, df):
        json = [{} for i in range(288)]
        for name, gp in df.groupby(['timestamp', 'newPlot']):
            time, plot = name
            if json[int(time)].__contains__(self.station2box[str(plot)]):  # 网格层次会重复
                json[int(time)][self.station2box[str(plot)]] += len(gp)
            else:
                json[int(time)][self.station2box[str(plot)]] = len(gp)

        self.saveJson(json,self.finalDir+'spaceVolumeDataset.json')


    def getOdMatrix(self,df):
        json = [{} for i in range(288)]
        total=0
        for name,gp in df.groupby(['imsi']):
            for i in range(len(gp)-1):
                x = gp.iloc[i]
                y = gp.iloc[i+1]
                time1 = int(x['timestamp'])
                time2 = int(y['timestamp'])
                if time1+1!=time2:
                    continue
                plot1 = self.station2box[str(int(x['newPlot']))]
                plot2 = self.station2box[str(int(y['newPlot']))]
                if plot1==plot2:
                    continue
                if not json[time1].__contains__(''+str(plot1)+'-'+str(plot2)):
                    json[time1][''+str(plot1)+'-'+str(plot2)]={'source': str(plot1), 'target': str(plot2), 'weight': 1}
                else:
                    json[time1][''+str(plot1)+'-'+str(plot2)]['weight']+=1
                total+=1
        temp = [[] for i in range(288)]
        for i in range(len(json)):  # time
            for key in json[i].keys():
                temp[i].append(json[i][key])
        print(total)
        self.saveJson(temp, self.finalDir + 'spaceOdDataset.json')




