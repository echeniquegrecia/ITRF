import math
import pyproj
from flask import Blueprint
from controllers.itrf_parameters.parameters import get_elipsoid_grs80
bp = Blueprint('Conventions', __name__)



def convert_to_geocentric_coordinates(lat, lon, h_elip, component):
    """Convert from geodetic coordinates to geocentric ones.

    :param lat: float, latitude in decimal degrees
    :param lon: float, longitude decimal degress
    :param h_elip: float, ellipsoid height in meters
    :param component: str, component of a geocentric vector
    :return: float, value in meters of a component of a geocentric vector.
    """

    #Convert lat degrees to radians
    lat_in_radians = lat * math.pi / 180

    #Convert long degrees to radians
    lon_in_radians = lon * math.pi / 180

    #Calcul of N
    a = get_elipsoid_grs80()['a']
    e2 = get_elipsoid_grs80()['e2']
    N = a / ((1 - e2 * (math.sin(lat_in_radians)) ** 2) ** (1 / 2))

    # Calcul of the geocentric coordinates X, Y and Z
    cos_lat = math.cos(lat_in_radians)
    cos_lon = math.cos(lon_in_radians)
    sin_lat = math.sin(lat_in_radians)
    sin_lon = math.sin(lon_in_radians)
    if component == 'X':
        X = (N + h_elip) * cos_lat * cos_lon
        return X
    elif component == 'Y':
        Y = (N + h_elip) * cos_lat * sin_lon
        return Y
    else:
        Z = ((1 - e2) * N + h_elip) * sin_lat
        return Z



def convert_from_dms_to_dd(coordinate):
    """Convert from degrees, minutes and second to decimal degress.

    :param coordinate: dict, it contains the degree, minute and second.
    :return: dict, it contains the decimal degress.
    """

    dict = {}
    if coordinate['degrees'] >= 0:
        dict['degrees_decimals'] = (coordinate['degrees'] + (coordinate['minutes'] / 60) + (coordinate['seconds'] / 3600))
    else:
        dict['degrees_decimals'] = (coordinate['degrees'] - (coordinate['minutes'] / 60) - (coordinate['seconds'] / 3600))
    return dict


def get_lat_long_h(X, Y, Z):
    """Get the geodetic coordinates (lat, long and h) from the geocentric ones.

    :param X: float, Geocentric component X
    :param Y: float, Geocentric component Y
    :param Z: float, Geocentric component Y
    :return: dict with the geodetic components.
    """

    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pyproj.transform(ecef, lla, X, Y, Z, radians=False)
    return {"lat":lat, "lon":lon, "h":alt}


def get_d_m_s(dd_value):
    """Convert degrees decimals to degrees, minutes and seconds.

    :param dd_value: float, decimal degrees
    :return: str, degrees, minutes and seconds.
    """

    degress = int(dd_value)
    if dd_value >= 0:
        minutes = int((dd_value - int(dd_value)) * 60)
        seconds = (((dd_value-int(dd_value))*60)-int(minutes))*60
    else:
        minutes = int((dd_value - int(dd_value)) * 60)*(-1)
        seconds = (((dd_value-int(dd_value))*60)+int(minutes))*60*(-1)
    results = str(degress) + " " + str(minutes) + " " + str(seconds)
    return results