from .gis_functions import Point

def normalise_lat(lat):
    return lat + 90

def normalise_lon(lon):
    return lon + 180

# calculate destination point, final bearing
def calculate_boundaries(point: Point, dist: float):

    p_north = point.destination_point(dist, 0)
    p_south = point.destination_point(dist, 180)
    p_east = point.destination_point(dist, 90)
    p_west = point.destination_point(dist, -90)

    return {
        "max_lat": normalise_lat(p_north.lat),
        "min_lat": normalise_lat(p_south.lat),
        "max_long": normalise_lon(p_east.lon),
        "min_long": normalise_lon(p_west.lon)
    }

