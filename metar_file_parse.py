from datetime import datetime
def text_file_parse(file, year = datetime.now().year, month = datetime.now().month):
    """ Takes a text file taken from the NOAA PORT system containing
    METAR data and creates a dataframe with all the observations

    parameters
    ----------
    file: string
          The path to the file containing the data. It should be extracted
          from NOAA PORT and NOT be in binary format

    return
    ---------
    df : pandas dataframe wtih the station id as the index

    """
    import pandas as pd
    import numpy as np
    from metar_decode import ParseError
    from metar_parse import parse_metar_to_named_tuple
    from process_stations import station_dict
    from datetime import datetime
    from calculations import altimeter_to_slp
    from metpy.units import units, pandas_dataframe_to_unit_arrays

    #Function to merge METARs
    def merge(x, key='     '):
        tmp = []
        for i in x:
            if (i[0:len(key)] != key) and len(tmp):
                yield ' '.join(tmp)
                tmp = []
            if i.startswith(key):
                i = i[5:]
            tmp.append(i)
        if len(tmp):
            yield ' '.join(tmp)

    #Open the file
    myfile = open(file)

    #Clean up the file and take out the next line (\n)
    value = myfile.read().rstrip()
    list_values = value.split(sep = '\n')
    list_values = list(filter(None, list_values))

    #Call the merge function and assign the result to the list of metars
    list_values = list(merge(list_values))

    #Remove the short lines that do not contain METAR observations or contain
    #METAR observations that lack a robust amount of data
    metars = []
    for metar in list_values:
        if len(metar) > 25:
            metars.append(metar)
    else:
        None

    #Create a dictionary with all the station name, locations, and elevations
    master = station_dict()

    #Setup lists to append the data to
    station_id = []
    lat = []
    lon = []
    elev = []
    date_time = []
    wind_dir = []
    wind_spd = []
    current_wx1= []
    current_wx2 = []
    current_wx3 = []
    skyc1 = []
    skylev1 = []
    skyc2 = []
    skylev2 = []
    skyc3 = []
    skylev3 = []
    skyc4 = []
    skylev4 = []
    cloudcover = []
    temp = []
    dewp = []
    altim = []
    current_wx1_symbol = []
    current_wx2_symbol = []
    current_wx3_symbol = []

    for metar in metars:
        try:
            metar = parse_metar_to_named_tuple(metar, master, year = year, month = month)
            station_id.append(metar.station_id)
            lat.append(metar.latitude)
            lon.append(metar.longitude)
            elev.append(metar.elevation)
            date_time.append(metar.date_time)
            wind_dir.append(metar.wind_direction)
            wind_spd.append(metar.wind_speed)
            current_wx1.append(metar.current_wx1)
            current_wx2.append(metar.current_wx2)
            current_wx3.append(metar.current_wx3)
            skyc1.append(metar.skyc1)
            skylev1.append(metar.skylev1)
            skyc2.append(metar.skyc2)
            skylev2.append(metar.skylev2)
            skyc3.append(metar.skyc3)
            skylev3.append(metar.skylev3)
            skyc4.append(metar.skyc4)
            skylev4.append(metar.skylev4)
            cloudcover.append(metar.cloudcover)
            temp.append(metar.temperature)
            dewp.append(metar.dewpoint)
            altim.append(metar.altimeter)
            current_wx1_symbol.append(metar.current_wx1_symbol)
            current_wx2_symbol.append(metar.current_wx2_symbol)
            current_wx3_symbol.append(metar.current_wx3_symbol)

        except ParseError:
            None

    col_units = {
    'station_id': None,
    'latitude': 'degrees',
    'longitude': 'degrees',
    'elevation': 'meters',
    'date_time': None,
    'wind_direction': 'degrees',
    'wind_speed': 'kts',
    'current_wx1': None,
    'current_wx2': None,
    'current_wx3': None,
    'skyc1': None,
    'skylev1': 'feet',
    'skyc2': None,
    'skylev2': 'feet',
    'skyc3': None,
    'skylev3': 'feet',
    'skyc4': None,
    'skylev4:': None,
    'cloudcover': None,
    'temperature': 'degC',
    'dewpoint': 'degC',
    'altimeter': 'inHg',
    'sea_level_pressure': 'hPa',
    'current_wx1_symbol': None,
    'current_wx2_symbol': None,
    'current_wx3_symbol': None,}

    df = pd.DataFrame({'station_id':station_id, 'latitude':lat, 'longitude':lon,
    'elevation':elev, 'date_time':date_time, 'wind_direction':wind_dir,
    'wind_speed':wind_spd, 'current_wx1':current_wx1, 'current_wx2':current_wx2,
    'current_wx3':current_wx3, 'skyc1':skyc1, 'skylev1':skylev1, 'skyc2':skyc2,
    'skylev2':skylev2, 'skyc3':skyc3, 'skylev3': skylev3, 'skyc4':skyc4,
    'skylev4':skylev4, 'cloudcover':cloudcover, 'temperature':temp, 'dewpoint':dewp,
    'altimeter':altim, 'current_wx1_symbol':current_wx2_symbol,
    'current_wx2_symbol':current_wx2_symbol, 'current_wx3_symbol':current_wx3_symbol},
    index = station_id)

    try:
        df['sea_level_pressure'] = altimeter_to_slp(
        altim * units('inHg'),
        elev * units('meters'),
        temp * units('degC')).magnitude
    except:
        df['sea_level_pressure'] = [np.nan]
    #Drop duplicates
    df = df.drop_duplicates(subset = ['date_time','latitude', 'longitude'], keep = 'last')

    df['altimeter'] = df.altimeter.round(2)
    df['sea_level_pressure'] = df.sea_level_pressure.round(2)

    #Convert the datetime string to a datetime object
    #df['date_time'] = pd.to_datetime(myfile.name[-17:-8] + df['time_utc'], format = "%Y%m%d_%H%M", exact=False)
    df.index = df.station_id

    #Set the units for the dataframe
    df.units = col_units
    pandas_dataframe_to_unit_arrays(df)

    return df
