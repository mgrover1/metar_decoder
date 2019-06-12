def altimeter_to_station_pressure(altim, elev):
    """ Convert the altimeter measurement to station pressure.

    This function is useful for working with METARs since most will provide
    altimeter values, but not sea level pressure or station pressure.

    The following definitions of altimeter setting and station pressure
    are taken from the Federal Meteorology Handbook (2013) p. 11-1

    Altimeter setting is the pressure value to which an aircraft altimeter scale
    is set so that it will indicate the altitude above mean sea level of an aircraft
    on the ground at the location for which the value is determined. It assumes a standard
    atmosphere.

    Station pressure is the atmospheric pressure at the designated station elevation

    Finding the station pressure can be helpful for calculating sea level pressure or
    other parameters.

    Parameters
    ----------
    altim : float or int with units
            The altimeter setting value as defined by the METAR or other observation,
            which can be measured in either inches of mercury (in. Hg) or millibars (hPa)
    elev: float or int with units
            Elevation of the station measuring pressure. This value will need to be in meters

    Returns
    --------

    station_pressure: float
            The station pressure in hPa, which can be used to calculate sea level pressure


    See Also
    ---------

    altimeter_sea_level_pressure

    Notes
    -------
    This function is implemented using the following equations from the Smithsonian Handbook (1951) p. 269

    Equation 1
    .. math:: A_{mb} = (p_{mb} - 0.3)F

    Equation 3
    .. math:: F = \left [1 + \left(\frac{p_{0}^n a}{T_{0}} \right) \frac{H_{b}}{p_{1}^n} \right ] ^ \frac{1}{n}

    Where

    p_{0} = standard sea level pressure = 1013.25 mb

    p_{1} = p_{mb} - 0.3 when p_{0} = 1013.25 mb

    a = lapse rate in NACA standard atmosphere below the isothermal layer 0.0065   ^{\circ}C. m.^{-1})

    T_{0} = standard sea-level temperature 288 K

    H_{b} = station elevation in meters (elevation for which station pressure is given)

    n = \frac{a R_{d}}{g} = 0.190284 where R_{d} is the gas constant for dry air

    And solving for p_{mb} results in the equation below, which is used to calculate station pressure (p_{mb})

    .. math:: p_{mb} = \left [A_{mb} ^ n - \left (\frac{p_{0} a H_{b}}{T_0} \right) \right] ^ \frac{1}{n} + 0.3

    """
    #Bring in the neccessary libraries
    from metpy.units import units
    import metpy.constants as mpconsts

    #Make sure the input values have the correct units
    altim = altim.to('hPa')
    elev = elev.to('meters')
    #Set the constant values

    #Mean Sea Level Pressure
    mslp = 1013.25 * units.hPa

    #Mean Sea Level Temperature
    mslt = 288 * units.kelvin

    #Lapse Rate in Standard Atmosphere
    a = 0.0065 * (units.delta_degC / units.m)

    #N value
    n = (mpconsts.Rd * a / mpconsts.g).to_base_units()

    station_pres = (altim ** n - ((mslp ** n * a * elev) / mslt)) ** (1/n) + (0.3 * units.hPa)

    return station_pres


from metpy.units import units
test = altimeter_to_station_pressure(1054.4*units.hPa, 1235*units.m)

def altimeter_to_slp(altim, elev, T):
    """

    :param altim:
    :param elev:
    :param T:
    :return:
    """
    #Bring in the neccessary libraries
    from metpy.units import units
    import metpy.constants as mpconsts
    from math import exp

    #Make sure the temperature is in Kelvin
    T = T.to('kelvin')

    #Make sure the elevation is measured in meters
    z = elev.to('meter')

    #Calculate the station pressure using the function altimeter_to_station_pressure()
    p = altimeter_to_station_pressure(altim, elev)

    #Calculate the scale height
    H = mpconsts.Rd * T / mpconsts.g

    #Calculate the pressure at sea level
    psl = p * exp(z/H)

    return psl

test = altimeter_to_slp(1054.4*units.hPa, 1235*units.m, 25*units.degC)
print(test)









    

