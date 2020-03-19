import json
import csv
import math
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

fileName = "data\\newStation.csv"
with open(fileName, newline='', encoding='UTF-8') as csvfile:
    rows = csv.reader(csvfile)
        
    lat = [41.08805847, 42.50167847]
    lng = [122.3507919, 124.00028229999998]
    # 122.3507919,41.40496826 122.8225937,41.08805847
    latStep = 0.008
    lngStep = 0.01
    
    boxes = []
    cnt = 0
    mp = set()
    
    ii = 0
    for row in rows:
        ii = ii + 1
        if ii == 1:#去除表头
            continue
        
        i = math.floor( (float(row[1]) - float(lat[0])) / latStep )
        j = math.floor( (float(row[0]) - float(lng[0])) / lngStep )
        
        if (i * 10000 + j) not in mp :
            tmp = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [lng[0] + j * lngStep, lat[0] + i * latStep],
                        [lng[0] + (j + 1) * lngStep, lat[0] + i * latStep],
                        [lng[0] + (j + 1) * lngStep, lat[0] + (i + 1) * latStep],
                        [lng[0] + j * lngStep, lat[0] + (i + 1) * latStep],
                        [lng[0] + j * lngStep, lat[0] + i * latStep],
                    ]],
                },
                "properties": {
                    "id": cnt,
                },
            }
            boxes.append(tmp)
            cnt = cnt + 1
            mp.add( (i * 10000 + j) )
    
    gridBoxed = {
        "type": "FeatureCollection",
        "features": boxes,
    }
    
    objectFileName = "data\\stationBoxes.json"
    with open(objectFileName, mode = 'w', encoding="utf-8") as json_file:
        json.dump(gridBoxed, json_file, ensure_ascii=False,  cls =NpEncoder)




















        
