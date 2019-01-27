from flask import request, Response
from controllers.email.send_email import send_email, remove_files
from controllers.itrf_transformation.transformation \
    import get_data_from_the_user, \
    get_geodetic_coordinates_in_dms, \
    get_geodetic_coordinates_in_dd, \
    get_geocentric_coordinates_in_epoch_begin, \
    get_geocentric_coordinates_in_epoch_final, \
    get_coordinates_transformed_to_ITRF_final
from controllers.velocity.velocity_calcul \
    import create_input_file_for_velocities
from settings import app


@app.route('/api/transformation/itrf', methods=['POST'])
def execute_itrf_transformation():
    """Get the data from the user and execute the ITRF transformation."""

    data = request.get_json()
    stations_list = get_data_from_the_user(
        data['file'],
        data['itrf_begin'],
        data['epoch_begin']
    )
    print("Get data from the user")
    geodetic_coordinates_list = get_geodetic_coordinates_in_dms(
        stations_list
    )
    print("Create the geodetic coordinates list")
    geodetic_coordinates_in_dd_list = get_geodetic_coordinates_in_dd(
        geodetic_coordinates_list
    )
    print("3 Convert geodetic coordinates in decimal degrees")
    create_input_file_for_velocities(
        data['filename'],
        geodetic_coordinates_in_dd_list
    )
    print("4 Creation of input file for velocity calculations")
    geocentric_coordinates_list = get_geocentric_coordinates_in_epoch_begin(
        geodetic_coordinates_in_dd_list
    )
    print("5 Calculate geocentric coordinates referred to the epoch begin")
    geocentric_coordinates_transformated_to_epoch_final = get_geocentric_coordinates_in_epoch_final(
        geocentric_coordinates_list, data['epoch_final'], data['filename']
    )
    print("6 Calculate geocentric coordinates referred to the epoch final")
    geocentric_coordinates_transformated_to_ITRF_final_list = get_coordinates_transformed_to_ITRF_final(
        geocentric_coordinates_transformated_to_epoch_final,
        data['epoch_begin'],
        data['itrf_final'],
        data['epoch_final']
    )
    print("7 Execute the ITRF transformation")
    send_email(geocentric_coordinates_transformated_to_ITRF_final_list, data)
    print("8 Send the result to the user's email")
    print("9 Remove files:")
    remove_files(data['file'], data['filename'])
    return Response(status=200)


if __name__ == '__main__':
    app.run()
