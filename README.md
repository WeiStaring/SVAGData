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
1. final/SpaceVolumeDataset.json。格式为[{},{},...,{}].有288个{}。json[i][j]表示第i个时间片内第j基站的流量，0<=i<288,0<=j<2793
2. 以5分钟为一片，离散化连续时间。则一天有288片。每片中的用户id和空间plot进行去重，否则会多重计数。以5分钟为一片，去重使得数据量从9800+->8100+。

# 空间流动数据集
1. finalData/spaceStayDataset.json 驻留数据集，json[i,j]表示第i个时间片内第j基站的驻留量
2. finalData/spaceTripDataset.json 出行数据集，json[i,j]表示第i个时间片内，边列表中索引为j的边的信息。信息格式为{source，target，weight}，表示一条从source到target的边，人数为3.
3. finalData/station2box.json 基站格子映射字典，每一个基站对应一个格子，每个格子对应多个基站
4. data/stationBoxes_0.008_0.01_653.json 格子位置，d3格式
5. 计算出行时，由于算法参数设置，会出现自环，我手动设置去除
6. 出行数据中，观察得到最大weight为3。

# tripmode文件夹：
1. TripMode.py计算出行方式，其返回值：1-驾车，2-步行，3-骑行，4-公交
2. TripModeResult.csv保存出行方式结果，存放在type列中
3. person1为其中一个人轨迹
4. Visualize可视化person1轨迹及其出行方式，结果在tripmode1.png中
5. newTripModeResult.csv中，distance为规划路线实际距离，duration为规划所需时间，speed为所选择的出行方式的速度，real_speed为实际速度
6. 由可视化结果可以看出，实际速度存在较多异常值， 实际所用时间与四种规划时间差距较大造成