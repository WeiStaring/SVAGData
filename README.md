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

##更新
1. 文档没写
2. travelPoint是出行数据，我想要找出行的起点plot，终点plot，起点时间和终点时间
3. 不同类之间的移动看做出行，例如t1时刻在类1中的p1，t2时刻在类2中的p2.t1t2相邻。则做一条出行记录R。记录t1，p1，t2，p2. 因此类1到类-1计一次出行，类1到类2也要记一次出行。不是仅仅把-1挑出来。之前是我疏忽了
4.改成文本时间也可以，但不利于计算，例如计算时间后把记录放入时间槽中，建议增加时间戳字段
5.计算stay时的plot，你用的众数。我还是建议求出几何平均，再计算最近欧式距离的基站做为plot
6. 三个csv放入resultData文件夹下

##tripmode文件夹：
1.TripMode.py计算出行方式，其返回值：1-驾车，2-骑行，3-步行，4-公交
2.TripModeResult.csv保存出行方式结果，存放在type列中
3.person1为其中一个人轨迹
4.Visualize可视化person1轨迹及其出行方式，结果在tripmode1.png中