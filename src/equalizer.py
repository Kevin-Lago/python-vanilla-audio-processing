def equalize(data):
    band1 = filter_band(data, 0, 640, 2)
    band2 = filter_band(data, 640, 1280, 2)
    band3 = filter_band(data, 1280, 1920, 2)
    band4 = filter_band(data, 1920, 2560, 2)
    band5 = filter_band(data, 2560, 3200, 2)
    band6 = filter_band(data, 3200, 3840, 0)
    band7 = filter_band(data, 3840, 4480, 0)
    band8 = filter_band(data, 4480, 5120, 0)
    band9 = filter_band(data, 5120, 5760, 0)
    band10 = filter_band(data, 5760, 6400, 0)

    return data