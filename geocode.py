import cPickle as pickle
import numpy as np
m = pickle.load(open("zip_grid.p","rb"))

def return_zip(m, lat, lon, nw_lat=40.917, nw_lon=-74.260, steps=0.002):
    """
    Returns zip code based on a grid search
    """
    lat, lon = float(lat), float(lon)     
    i, j = int((nw_lat - lat)/steps), int((lon - nw_lon)/steps)
    try:
        return m[i][j]
    except:
        return -1
        
