def findPlot(lat, lon, station):
    station['x'] = lat - station['latitude']
    station['y'] = lon - station['longitude']
    station['dist'] = station['x'] ** 2 + station['y'] ** 2
    id = station['dist'].idxmin()

    return id

