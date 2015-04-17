import numpy as np
import re
from geopy.geocoders import Nominatim

def parse_zip(address):

    try:
        return int(re.findall(r"[0-1][0-9]{4},", address)[0][:5])
    except:
        return -1
        
def make_str(lat_lon):
    return ",".join(map(str, lat_lon))
    
def create_grid(geolocator, nw_lat_lon, se_lat_lon, steps):
    """
    Create a grid of zip codes based on lat long
    nw_lat_lon = list of lat long coordinates for north west corner
    se_lat_lon = list of lat long coordinates for south west corner
    steps = size of each lat-long step
    """
    m = np.zeros((int((nw_lat_lon[0]-se_lat_lon[0])/steps), 
                 int((se_lat_lon[1]-nw_lat_lon[1])/steps)), dtype=int)
    for i in xrange(m.shape[0]):
        for j in xrange(m.shape[1]):
            location = geolocator.reverse(make_str([nw_lat_lon[0]-steps*i,se_lat_lon[1]+steps*j]))  
            z = parse_zip(location.address)
            print location.address
            m[i][j] = z            
    return m

def return_zip(m, lat, lon, nw_lat=40.917577, nw_lon=-74.25909, steps=0.001):
    """
    Returns zip code based on a grid search
    """
    lat, lon = float(lat), float(lon)     
    i, j = int((nw_lat - lat)/steps), int((lon - nw_lon)/steps)
    try:
        return m[i][j]
    except:
        return -1
    
def main():
    #boundary info from
    #http://www.maptechnica.com/us-city-boundary-map/city/New%20York/state/NY/cityid/3651000
    nw_lat_lon = [40.917577, -74.25909] #NW boundary of NYC (includes some part of NJ)
    se_lat_lon = [40.477399, -73.70027] #SE boundary of NYC 
    steps = 0.001 
    geolocator = Nominatim(timeout=100)
    m = create_grid(geolocator, nw_lat_lon, se_lat_lon, steps)
    #test a bunch of lat longs
   
    print("Grid: %d, Actual: %d " % (return_zip(m, 40.90542,-73.97521),
                                     parse_zip(geolocator.reverse(make_str([40.90542,-73.97521])).address)))    
    print("Grid: %d, Actual: %d " % (return_zip(m, 40.900,-73.621),
                                     parse_zip(geolocator.reverse(make_str([40.900,-73.621])).address)))
    print("Grid: %d, Actual: %d " % (return_zip(m, 40.542,-74.1),
                                     parse_zip(geolocator.reverse(make_str([40.542,-74.1])).address)))                                     
    #test out of bound lat longs
    return_zip(m, 41.90542,-73.97521) 
    return_zip(m, 40.90542,-72.97521) 
    return_zip(m, 40.90542,-75.97521) 
    return_zip(m, 39.00542,-73.97521) 
    return m
