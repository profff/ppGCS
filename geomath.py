import math


EARTH_RADIUS=6.3781e6

def getDistanceClose(slat,slon,elat,elon):
    dlat = elat - slat
    dlong = elon - slon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def getMeters(olat,olon,fixlat,fixlon):
    dlat = fixlat-olat
    dlon = fixlon-olon
    return (dlon*1.113195e5,dlat*1.113195e5)

def geoFromPtByDistance(lat,lon,heading,dist):
    dr=dist/EARTH_RADIUS

    st_rlat=math.radians(lat)
    st_rlon=math.radians(lon)
    st_rhead=math.radians(heading)
    
    dt_lat=math.asin(   math.sin(st_rlat)*math.cos(dr)+
                        math.cos(st_rlat)*math.sin(dr)*math.cos(st_rhead))
    dt_lon=st_rlon+math.atan2(  math.sin(st_rhead)*math.sin(dr)*math.cos(st_rlat),
                                math.cos(dr)-math.sin(st_rlat)*math.sin(dt_lat))
    dt_lat=math.degrees(dt_lat)
    dt_lon=math.degrees(dt_lon)
    return (dt_lat,dt_lon)
