import os
from settings import velocity_input
from flask import Blueprint
from settings import velocity_output, vemos2009_vx, vemos2009_vy, vemos2009_vz
bp = Blueprint('Velocities', __name__)


def execute_gmt_commands(velocity_file_input_file, filename_excel):
    os.system("gmt grdtrack " + velocity_file_input_file + " -G" + vemos2009_vx + " >" + velocity_output + "/" + filename_excel + "_vx.output")
    os.system("gmt grdtrack " + velocity_file_input_file + " -G" + vemos2009_vy + " >" + velocity_output + "/" + filename_excel + "_vy.output")
    os.system("gmt grdtrack " + velocity_file_input_file + " -G" + vemos2009_vz + " >" + velocity_output + "/" + filename_excel + "_vz.output")


def create_input_file_for_velocities(filename_excel, get_geodetic_coordinates_in_dd):
    """Create the input file for the velocities calculations.

    :param filename_excel: str, name of the Excel file sent by the user
    :param get_geodetic_coordinates_in_dd: list of the geodetic coordinates in decimal degrees
    :return: str, message to notify that the input file to calculate velocity is created.
    """

    velocity_file_input_path = velocity_input + "/" + filename_excel + "_v_input.txt"
    velocity_file_input_file = open(velocity_file_input_path , "w")
    for station in get_geodetic_coordinates_in_dd:
        velocity_file_input_file.write(str(station['lon']['degrees_decimals']) + "  " +  str(station['lat']['degrees_decimals'])+"\n")
    velocity_file_input_file.close()
    execute_gmt_commands(velocity_file_input_path, filename_excel)
    return "File input for velocity created"


def get_velocities_from_output_file(file):
    """Read and get all the the velocity values of a component from output file velocity.

    :param file: str, file to read
    :return: list with all the velocity values of a component
    """

    f = open(file, "r")
    lines = f.readlines()
    velocities_list = []
    for x in lines:
        velocity = x.split('\t\t')[1]
        velocity = float(velocity)
        velocities_list.append(float(velocity))
    f.close()
    return velocities_list



def get_velocity_components(filename_excel):
    """Get the velocity components (vx, vy and vz) at all stations.

    :param filename_excel: str, name of the Excel file sent by the user.
    :return: dict with all the velocity components at each station.
    """

    file_vx = velocity_output + "/" + filename_excel + "_vx.output"
    file_vy = velocity_output + "/" + filename_excel + "_vy.output"
    file_vz = velocity_output + "/" + filename_excel + "_vz.output"
    dict = {}
    dict['vx'] = get_velocities_from_output_file(file_vx)
    dict['vy'] = get_velocities_from_output_file(file_vy)
    dict['vz'] = get_velocities_from_output_file(file_vz)
    return dict