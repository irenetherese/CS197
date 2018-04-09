import os
import numpy as np


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def lon_lat_to_cartesian(lat, lon):
    R = 6378137  # Radius of the earth
    lon_r = np.radians(lon)
    lat_r = np.radians(lat)

    x = R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)
    return x, y, z


def cartesian_to_lon_lat(coords):
    x = coords[0]
    z = coords[2]
    R = 6378137

    lat_r = np.arcsin(z / R)
    lon_r = np.arccos(x / (R * np.cos(lat_r)))

    lat = np.degrees(lat_r)
    lon = np.degrees(lon_r)

    return lat, lon

    # print(lon_lat_to_cartesian(14.57343263,120.9975392))
    # print(cartesian_to_lon_lat(lon_lat_to_cartesian(14.57343263,120.9975392)))
