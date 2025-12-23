from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lng1, lat2, lng2):
    lon1, lat1, lon2, lat2 = map(
        radians, [lng1, lat1, lng2, lat2]
    )

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km
