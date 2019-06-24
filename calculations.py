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

def altimeter_to_slp(altim, elev, T):
    """ Convert the altimeter setting to sea level pressure.

    This function is useful for working with METARs since most will provide
    altimeter values, but not sea level pressure, which is often plotted
    on surface maps.

    The following definitions of altimeter setting, station pressure, and
    sea level pressure are taken from the Federal Meteorology Handbook (2013)
    p.11-1

    Altimeter setting is the pressure value to which an aircraft altimeter scale
    is set so that it will indicate the altitude above mean sea level of an aircraft
    on the ground at the location for which the value is determined. It assumes a standard
    atmosphere.

    Station pressure is the atmospheric pressure at the designated station elevation.

    Sea-level pressure is a pressure value obtained by the theoretical reduction of barometric
    pressure to sea level. It is assumed that atmosphere extends to sea level below the station
    and that the properties of the atmosphere are related to conditions observed at the station.
    This value is recorded by some surface observation stations, but not all. If the value is
    recorded, it can be found in the remarks section.

    Finding the sea level pressure is helpful for plotting purposes and different calculations.

    Parameters
    ----------
    altim : float or int with units
            The altimeter setting value is defined by the METAR or other observation,
            with units of inches of mercury (in Hg) or millibars (hPa)
    elev  : float or int with units
            Elevation of the station measuring pressure. Often times measured in meters
    T     : float or int with units
            Temperature at the station measured in either Celsius or Fahrenheit

    Returns
    -------

    sea_level_pressure: float
            The sea level pressur in hPa, which is often times plotted on surface maps
            and makes pressure values easier to compare between different stations


    See Also
    --------
    altimeter_to_station_pressure

    Notes
    -------
    This function is implemented using the following equations from Wallace and Hobbs (1977)

    Equation 2.29
    .. math:: \Delta z = Z_{2} - Z_{1} = \frac{R_{d} \bar T_{v}}{g_0}ln\left(\frac{p_{1}}{p_{2}} \right) = \bar H ln \left (\frac {p_{1}}{p_{2}} \right)

    Equation 2.31
    .. math:: p_{0} = p_{g}exp \left(\frac{Z_{g}}{\bar H} \right) = p_{g} exp \left(\frac{g_{0}Z_{g}}{R_{d}\bar T_{v}} \right)

    Then by subsituting Delta Z for Z_{g} in Equation 2.31, we get

    .. math:: p_{sea level} = p_{station} exp\left(\frac{\Delta z}{H}\right)

    where Delta_Z is the elevation in meters and H = \frac{R_{d}T}{g}
    """
    #Bring in the neccessary libraries
    from metpy.units import units
    import metpy.constants as mpconsts
    from numpy import exp

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
