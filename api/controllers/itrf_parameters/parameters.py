def get_transformation_parameters():
    """Return the transformation parameters from ITRF2008 to ITRF1994."

    These parameters were obtained from the ITRF official website, except for
    'final_epoch', this last parameter change according to the final epoch set by the user.
    For more information, go to http://itrf.ensg.ign.fr/

    """

    parameters = {}
    # The units of TX,TY and TZ are in millimeters (mm)
    parameters['TX'] = 4.8
    parameters['TY'] = 2.6
    parameters['TZ'] = -33.2
    # The units of TX,TY and TZ rate are in millimeters by year (mm/y)
    parameters['TX_rate'] = 0.1
    parameters['TY_rate'] = -0.5
    parameters['TZ_rate'] = -3.2
    # The units of RX,RY and RZ are in seconds (")
    parameters['RX'] = 0
    parameters['RY'] = 0
    parameters['RZ'] = 0.06
    # The units of RX,RY and RZ rate are in seconds by year ("/y)
    parameters['RX_rate'] = 0
    parameters['RY_rate'] = 0
    parameters['RZ_rate'] = 0.02
    # The unit of S is in ppb
    parameters['S'] = 2.92
    # The unit of S rate is in ppb/year
    parameters['S_rate'] = 0.09
    # Epoch
    parameters['itrf_2008_epoch'] = 2000.0
    # Final Epoch
    parameters['final_epoch'] = 1995.4
    return parameters


def get_elipsoid_grs80():
    """Return  a dict with the GRS80 ellipsoid parameters."""

    data = {}
    # Equatorial radius of the Earth
    data['a']= 6378137
    # Flattening
    data['f'] = (1 / 298.257223563)
    # First excentricity
    data['e2'] = 2 * data['f'] - data['f'] ** 2
    return data