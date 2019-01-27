import json
import os
import pandas
from flask_mail import Message
from controllers.email.message_email import make_email_message
from settings import data_output, app, mail, velocity_input, velocity_output


def send_email(geocentric_coordinates_transformated_to_ITRF_final_list, data):
    """Send the result of the ITRF transformation to the user's email.

    :param geocentric_coordinates_transformated_to_ITRF_final_list: list with the result of the ITR transformation
    :param data: dict, it contains the epochs, ITRFs and velocity model set by the user.
    """
    pandas.read_json(json.dumps(geocentric_coordinates_transformated_to_ITRF_final_list)).to_excel(
        data_output + "/" + data['filename'] + "_results.xlsx")
    msg = Message('ITRF Transformations', sender=app.config['MAIL_USERNAME'], recipients=[data['email']])
    msg.body = make_email_message(data['itrf_begin'], data['epoch_begin'], data['itrf_final'], data['epoch_final'],
                                  data['velocity'], data['date'])
    with app.open_resource(data_output + "/" + data['filename'] + "_results.xlsx") as fp:
        file_name = data['filename'] + "_results"
        msg.attach(file_name + ".xlsx", file_name + "/xlsx", fp.read())
    mail.send(msg)


def remove_files(file, filename_excel):
    """Remove all the files generated during the ITRF transformation.

    :param file: str
    :param filename_excel:
    """
    os.remove(file)
    print("Remove the data input sent by the user")
    os.remove(velocity_input + "/" + filename_excel + "_v_input.txt")
    print("Remove the input file for velocity calculations")
    os.remove(velocity_output + "/" + filename_excel + "_vx.output")
    print("Remove the vx output file")
    os.remove(velocity_output + "/" + filename_excel + "_vy.output")
    print("Remove the vy output file")
    os.remove(velocity_output + "/" + filename_excel + "_vz.output")
    print("Remove the vy output file")
    os.remove(data_output + "/" + filename_excel + "_results.xlsx")
    print("Remove the data output sent to the user's email.")