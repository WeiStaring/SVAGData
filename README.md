#项目结构
## data
用以存储原始数据和加工中的数据
1. data.csv:原始数据
2. dataAfterWash.cdv：粗加工数据
3. station.csv：基站数据，长度2793
4. vehicle.csv：交通站点数据
5.drop_duplicates_station.csv 新基站数据，位置相同基站的newPlot字段相同，长度2793
## dataModel
用以存储数据处理模型
1. BaseModel：数据处理基类和粗加工模型
2. SpaceFlowModel：空间流量分布数据模型
3. VisualModel：数据分析模型（出图形）
    1. 
## images
用以存储结果图片
## resultData
用以存储加工终点的数据集
1. newStation.csv drop_duplicates_station.csv相同位置去重，长度1519
# 粗加工
和参考的数据清洗规则有基础不同点如下
1. 时间使用时间戳，而非20181003....，原因是虽然后者容易理解，但不容易转化。而前者易计算，需要时可以一步转化为后者
2. 修改了地点表示，station.csv中的基站编号冗长，用数字编码代替。我同时修改了station和dataAfterWash中的地点表示。因为这样不仅节省空间，而且把离散变量转化成了连续变量，在数据存储和未来d3代码中都比较方便直接代替索引
# 空间流量数据集
1. SpaceFlowDataset.json。格式为[{},{},...,{}].有288个{}。json[i][j]表示第i个时间片内第j基站的流量，0<=i<288,0<=j<2793
2. 以5分钟为一片，离散化连续时间。则一天有288片。每片中的用户id和空间plot进行去重，否则会多重计数。以5分钟为一片，去重使得数据量从9800+->8100+。