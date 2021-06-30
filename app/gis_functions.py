import math
import numpy as np
from astropy.constants import R_earth

R_EARTH = R_earth.value

class Point():
    def __init__(self, lat, lon) -> None:
        self.lat = float(lat)
        self.lon = float(lon)


    def destination_point(self, distance: float, compass_bearing: float) -> 'Point':
        bearing = np.radians(compass_bearing)
        lat_radians = np.radians(self.lat)
        lon_radians = np.radians(self.lon)

        lat2_radians = math.asin( math.sin(lat_radians)*math.cos(distance/R_EARTH) +
            math.cos(lat_radians)*math.sin(distance/R_EARTH)*math.cos(bearing))

        lon2_radians = lon_radians + math.atan2(math.sin(bearing)*math.sin(distance/R_EARTH)*math.cos(lat_radians),
                    math.cos(distance/R_EARTH)-math.sin(lat_radians)*math.sin(lat2_radians))

        lat2 = np.degrees(lat2_radians)
        lon2 = np.degrees(lon2_radians)

        return Point(lat2,lon2)
