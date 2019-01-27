import xlrd
import math
from collections import OrderedDict
from controllers.itrf_parameters.parameters import get_transformation_parameters
from controllers.convertions.convertions import convert_from_dms_to_dd, convert_to_geocentric_coordinates, \
    get_d_m_s, get_lat_long_h
from controllers.velocity.velocity_calcul import get_velocity_components


def get_data_from_the_user(file, itrf_begin, epoch_begin):
    """Get the input geodetic coordinates from the Excel file sent by the user.

    :param file: str, Excel file sent by the user with the input geodetic coordinates
    :param itrf_begin: int, year of the frame (ITRF). Example: 2000, 2005, 2008
    :param epoch_begin: float, measurement epoch of the stations.
    :return: list of the input geodetic coordinates to transform.
    """

    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    stations_list = []
    for row in range(1, sheet.nrows):
        row_values = sheet.row_values(row)
        station = OrderedDict()
        station['id'] = row-1
        station['station'] = row_values[0]
        station['lat'] = row_values[1]
        station['lon'] = row_values[2]
        station['h_elip'] = row_values[3]
        station['itrf_begin'] = itrf_begin
        station['epoch_begin'] = epoch_begin
        stations_list.append(station)
    return stations_list


def get_translation_to_epoch_final(epoch_begin):
    """Get the translation to the epoch final.

    :param epoch_begin: float, measurement epoch.
    :return: dict with the X, Y and Z translations to the final epoch.
    """

    TX = get_transformation_parameters()['TX']
    TX_rate = get_transformation_parameters()['TX_rate']
    TY = get_transformation_parameters()['TY']
    TY_rate = get_transformation_parameters()['TY_rate']
    TZ = get_transformation_parameters()['TZ']
    TZ_rate = get_transformation_parameters()['TZ_rate']
    transl_to_epoch_final = {}
    transl_to_epoch_final['TX_final_epoch'] = (TX + (
            TX_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch'])+ TX_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch'])
    ))/1000
    transl_to_epoch_final['TY_final_epoch'] = (TY + (
            TY_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch']) + TY_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch'])
    ))/1000
    transl_to_epoch_final['TZ_final_epoch'] = (TZ + (
                TZ_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch']) + TZ_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch'])
    ))/1000

    return transl_to_epoch_final


def get_rotation_to_epoch_final(epoch_begin):
    """Get the rotation to the epoch final.

    :param epoch_begin: float, measurement epoch.
    :return: dict with the X, Y and Z rotations to the final epoch.
    """

    RX = get_transformation_parameters()['RX']
    RX_rate = get_transformation_parameters()['RX_rate']
    RY = get_transformation_parameters()['RY']
    RY_rate = get_transformation_parameters()['RY_rate']
    RZ = get_transformation_parameters()['RZ']
    RZ_rate = get_transformation_parameters()['RZ_rate']
    mt = (0.001/3600)*(math.pi/180)
    rot_to_epoch_final = {}
    rot_to_epoch_final['RX_final_epoch'] = (RX + (
            RX_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch'])+ RX_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch']))
    )*mt
    rot_to_epoch_final['RY_final_epoch'] = (RY + (
            RY_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch']) + RY_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch']))
    )*mt
    rot_to_epoch_final['RZ_final_epoch'] = (RZ + (
                RZ_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch']) + RZ_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch']))
    )*mt

    return rot_to_epoch_final


def get_scale_to_epoch_final(epoch_begin):
    """Get the scale to the final epoch

    :param epoch_begin: float, measurement epoch
    :return: dict with scale to the final epoch.
    """

    S = get_transformation_parameters()['S']
    S_rate = get_transformation_parameters()['S_rate']
    s_to_epoch_final = {}
    s_to_epoch_final['S_final_epoch'] = S + (
            S_rate * (get_transformation_parameters()['final_epoch'] - get_transformation_parameters()['itrf_2008_epoch'])+ S_rate * (epoch_begin - get_transformation_parameters()['itrf_2008_epoch'])
    )
    return s_to_epoch_final


def get_geodetic_coordinates_in_dms(data_from_the_user):
    """Get geodetic coordinates in degrees, minutes and seconds.

    :param data_from_the_user: list of the input geodetic coordinates to transform.
    :return: list of the geodetic coordinates in degrees, minutes and seconds.
    """

    list_geodetic_coordinates = []
    for station in data_from_the_user:
        station_dict = {}
        value = station['lat']
        value = value.split()
        value1 = station['lon']
        value1 = value1.split()
        station_dict['id'] = int(station['id'])
        station_dict['station'] = str(station['station'])
        station_dict['lat'] = {'degrees':int(value[0]), 'minutes': int(value[1]), 'seconds':float(value[2])}
        station_dict['lon'] = {'degrees': int(value1[0]), 'minutes': int(value1[1]), 'seconds': float(value1[2])}
        station_dict['h_elip'] = float(station['h_elip'])
        station_dict['itrf_begin'] = int(station['itrf_begin'])
        station_dict['epoch_begin'] = float(station['epoch_begin'])
        list_geodetic_coordinates.append(station_dict)
    return list_geodetic_coordinates



def get_geodetic_coordinates_in_dd(get_input_geodetic_coordinates_in_dms):
    """Get input geodetic coordinates in decimal degrees.

    :param get_input_geodetic_coordinates_in_dms: list of the geodetic coordinates in degrees, minutes and seconds
    :return: list of the geodetic coordinates in decimal degrees.
    """

    geodetic_coordinates_in_dd_list = []
    for station in get_input_geodetic_coordinates_in_dms:
        dict = {}
        dict['id'] = station['id']
        dict['station'] = station['station']
        dict['lat'] = convert_from_dms_to_dd(station['lat'])
        dict['lon'] = convert_from_dms_to_dd(station['lon'])
        dict['h_elip'] = station['h_elip']
        dict['itrf_begin'] = station['itrf_begin']
        dict['epoch_begin'] = station['epoch_begin']
        geodetic_coordinates_in_dd_list.append(dict)
    return geodetic_coordinates_in_dd_list

def get_geocentric_coordinates_in_epoch_begin(get_dd_geodetic_coordinates):
    """Get the geocentric coordinates referred to the epoch begin.

    :param get_dd_geodetic_coordinates: list of the geodetic coordinates in decimal degrees
    :return: list of the geocentric coordinates referred to the epoch begin.
    """

    geocentric_coordinates_list = []
    for station in get_dd_geodetic_coordinates:
        dict = {}
        dict['id'] = station['id']
        dict['station'] = station['station']
        dict['X'] = convert_to_geocentric_coordinates(
            station['lat']['degrees_decimals'], station['lon']['degrees_decimals'], station['h_elip'], 'X'
        )
        dict['Y'] = convert_to_geocentric_coordinates(
            station['lat']['degrees_decimals'], station['lon']['degrees_decimals'], station['h_elip'], 'Y'
        )
        dict['Z'] = convert_to_geocentric_coordinates(
            station['lat']['degrees_decimals'], station['lon']['degrees_decimals'], station['h_elip'], 'Z'
        )
        dict['itrf_begin'] = station['itrf_begin']
        dict['epoch_begin'] = station['epoch_begin']
        geocentric_coordinates_list.append(dict)
    return geocentric_coordinates_list


def get_geocentric_coordinates_in_epoch_final(get_geocentric_coordinates_in_epoch_begin, epoch_final, filename_excel):
    """Get the geocentric coordinates referred to the epoch final.

    :param get_geocentric_coordinates_in_epoch_begin: list of the geocentric coordinates referred to the epoch begin
    :param epoch_final: float, epoch final of the transformation
    :param filename_excel: str, name of the Excel file sent by the user.
    :return: list with the geocentric coordinates referred to epoch final for each station.
    """

    get_geocentric_coordinates_in_epoch_final_list = []
    for station in get_geocentric_coordinates_in_epoch_begin:
        dict = {}
        dict['station'] = station['station']
        dict['id'] = station['id']
        dict['X'] = station['X'] + get_velocity_components(filename_excel)['vx'][station['id']] * (epoch_final - station['epoch_begin'])
        dict['Y'] = station['Y'] + get_velocity_components(filename_excel)['vy'][station['id']] * (epoch_final - station['epoch_begin'])
        dict['Z'] = station['Z'] + get_velocity_components(filename_excel)['vz'][station['id']] * (epoch_final - station['epoch_begin'])
        dict['itrf_begin'] = station['itrf_begin']
        dict['epoch_final'] = epoch_final
        get_geocentric_coordinates_in_epoch_final_list.append(dict)
    return get_geocentric_coordinates_in_epoch_final_list


def get_coordinates_transformed_to_ITRF_final(
        get_geocentric_coordinates_in_epoch_final,epoch_begin, itrf_final,epoch_final):
    """Get the geocentric and geodetic coordinates referred to the ITRF final.

    :param get_geocentric_coordinates_in_epoch_final: list with the geocentric coordinates referred to epoch final for each station
    :param epoch_begin: float, measurement epoch.
    :param itrf_final: int, year of the frame (ITRF). Example: 1994, 2000, 2005
    :param epoch_final: float, epoch final of the transformation
    :return: list with the geocentric and geodetic coordinates referred to the ITRF final.
    """

    S = get_transformation_parameters()['S']
    s = get_transformation_parameters()['S_rate']
    scale = (S+(s*(epoch_final - get_transformation_parameters()['itrf_2008_epoch'])+s*(epoch_begin - get_transformation_parameters()['itrf_2008_epoch'])))*0.000000001
    get_coordinates_transformed_to_ITRF_final_list = []
    Tx = get_translation_to_epoch_final(epoch_begin)['TX_final_epoch']
    Ty = get_translation_to_epoch_final(epoch_begin)['TY_final_epoch']
    Tz = get_translation_to_epoch_final(epoch_begin)['TZ_final_epoch']
    Rx = get_rotation_to_epoch_final(epoch_begin)['RX_final_epoch']
    Ry = get_rotation_to_epoch_final(epoch_begin)['RY_final_epoch']
    Rz = get_rotation_to_epoch_final(epoch_begin)['RZ_final_epoch']
    for station in get_geocentric_coordinates_in_epoch_final:
        dict = {}
        dict['station'] = station['station']
        dict['X'] = Tx + (1 + scale) * station['X'] + Rx * station['Y'] - Ry * station['Z']
        dict['Y'] = Ty - Rz * station['X'] + (1 + scale) * station['Y'] + Rz * station['Z']
        dict['Z'] = Tz + Ry * station['X'] - Rx * station['Y'] + (1 + scale) * station['Z']
        dict['lat'] = get_d_m_s(get_lat_long_h(dict['X'], dict['Y'], dict['Z'])['lat'])
        dict['lon'] = get_d_m_s(get_lat_long_h(dict['X'], dict['Y'], dict['Z'])['lon'])
        dict['h_elip'] = get_lat_long_h(dict['X'], dict['Y'], dict['Z'])['h']
        dict['itrf_final'] = itrf_final
        dict['epoch_final'] = epoch_final
        get_coordinates_transformed_to_ITRF_final_list.append(dict)
    return get_coordinates_transformed_to_ITRF_final_list
