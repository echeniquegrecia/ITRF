def make_email_message(itrf_begin, epoch_begin, itrf_final, epoch_final, velocity, date):
    """Make the email message that will be sent to the user when the ITRF transformation is successful.

    :param itrf_begin: int,
    :param epoch_begin: float,
    :param itrf_final: int,
    :param epoch_final:float,
    :param velocity: str,
    :param date: str,
    :return: str, email message.
    """

    message = "Estimado Usuario,\n\nEn adjunto encontrará los resultados de la transformacion ITRF de acuerdo a la siguiente configuración:\n\nITRF inicial: "+str(itrf_begin)+"\nEpoca inicial: "+str(epoch_begin)+"\nITRF final: "+str(itrf_final)+"\nEpoca final: "+str(epoch_final)+"\nModelo de velocidad: "+velocity+"\nFecha de la solicitud de la transformación: "+date+"\n\n\nSaludos Cordiales,\n\nEquipo de Geodesia del IGVSB."
    return message