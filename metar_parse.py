def parse_metar(metar_text):
    """Takes in a metar file, in a text form, and creates a pandas
    dataframe that can be easily subset

    Input:
    metar_text = string with the METAR data

    Output:
    Pandas Dataframe that can be subset easily
    """

    # Import the neccessary libraries
    import pandas as pd
    import numpy as np
    from metar_decode import parse
    from metpy.units import units
    from process_stations import StationLookup

    # Build a dataframe that will store the data
    df = pd.DataFrame()

    #Setup the dictionary containing the latitude and longitude data for stations
    master = StationLookup().sources[0][1]
    for station in StationLookup().sources:
        master = {**master, **station[1]}

    # Decode the data using the parser (built using Canopy)
    tree = parse(metar_text)

    # Set the station id
    if tree.siteid.text == '':
        df['station_id'] = [np.nan]
    else:
        df['station_id'] = [tree.siteid.text]
        #Extract the latitude and longitude values from "master" dictionary
        try:
            df['lat'] = [master[tree.siteid.text.strip()].latitude]
            df['lon'] = [master[tree.siteid.text.strip()].longitude]
        except:
            df['lat'] = [np.nan]
            df['lon'] = [np.nan]

    # Set the datetime
    if tree.datetime.text == '':
        df['date_time'] = [np.nan]
        df['day'] = [np.nan]
        df['time_utc'] = [np.nan]
    else:
        datetime = tree.datetime.text[:-1]
        df['date_time'] = [datetime]
        df['day'] = [int(datetime[0:3])]
        df['time_utc'] = [int(datetime[3:])]

    # Set the wind variables
    if tree.wind.text == ('' or "/////KT"):
        df['wind_dir'] = [np.nan]
        df['wind_spd'] = [np.nan]
    else:
        if tree.wind.wind_dir.text == ('VRB' or 'VAR'):
            df['wind_dir'] = [np.nan]
            df['wind_spd'] = [float(tree.wind.wind_spd.text)]
        else:
            df['wind_dir'] = [int(tree.wind.wind_dir.text)]
            df['wind_spd'] = [int(tree.wind.wind_spd.text)]

    # Set the weather symbols
    if tree.curwx.text == '':
        df['wx1'] = [np.nan]
        df['wx2'] = [np.nan]
    else:
        wx = [np.nan, np.nan]
        wx[0:len((tree.curwx.text.strip()).split())] = tree.curwx.text.strip().split()
        df['wx1'] = [wx[0]]
        df['wx2'] = [wx[1]]

    # Set the sky conditions
    if tree.skyc.text == '':
        df['skyc1'] = [np.nan]
        df['skyc2'] = [np.nan]
        df['skyc3'] = [np.nan]
    elif tree.skyc.text.strip()[0:2] == 'VV':
        df['skyc1'] = 'VV'
        df['skylev1'] = tree.skyc.text.strip()[2:]
    else:
        skyc = [np.nan, np.nan, np.nan, np.nan]
        skyc[0:len((tree.skyc.text.strip()).split())] = tree.skyc.text.strip().split()
        try:
            df['skyc1'] = [skyc[0][0:3]]
            df['skylev1'] = [float(skyc[0][3:])*100]

        except:
            df['skyc1'] = [np.nan]
            df['skylev1'] = [np.nan]
        try:
            df['skyc2'] = [skyc[1][0:3]]
            df['skylev2'] = [float(skyc[1][3:])*100]
        except:
            df['skyc2'] = [np.nan]
            df['skylev2'] = [np.nan]
        try:
            df['skyc3'] = [skyc[2][0:3]]
            df['skylev3'] = [float(skyc[2][3:])*100]
        except:
            df['skyc3'] = [np.nan]
            df['skylev3'] = [np.nan]
        try:
            df['skyc4'] = [skyc[3][0:3]]
            df['skylev4'] = [float(skyc[3][3:])*100]
        except:
            df['skyc4'] = [np.nan]
            df['skylev4'] = [np.nan]

    if df['skyc1'].values[0] == ('SKC' or 'NCD' or 'CLR' or 'NSC'):
        df['cloudcover'] = 0
    elif df['skyc1'].values[0] == 'FEW':
        df['cloudcover'] = 2
    elif df['skyc1'].values[0] == 'SCT':
        df['cloudcover'] = 4
    elif df['skyc1'].values[0] == 'BKN':
        df['cloudcover'] = 6
    elif df['skyc1'].values[0] == ('OVC' or 'VV'):
        df['cloudcover'] = 8
    else:
        df['cloudcover'] = np.nan



    # Set the temperature and dewpoint
    if tree.temp_dewp.text == ('' or ' MM/MM'):
        df['temp'] = [np.nan]
        df['dewp'] = [np.nan]
    else:
        if "M" in tree.temp_dewp.temp.text:
            df['temp'] = [(-1 * float(tree.temp_dewp.temp.text[-2:]))]
        else:
            df['temp'] = [float(tree.temp_dewp.temp.text[-2:])]
        if "M" in tree.temp_dewp.dewp.text:
            df['dewp'] = [(-1 * float(tree.temp_dewp.dewp.text[-2:]))]
        else:
            df['dewp'] = [float(tree.temp_dewp.dewp.text[-2:])]

    # Set the altimeter value
    if tree.altim.text == '':
        df['altim'] = [np.nan]
    else:
        if (float(tree.altim.text[2:6])) > 1100:
            df['altim'] = [int((float(tree.altim.text[2:6]) / 100) * units("inHg").to('hPa').magnitude)]
        else:
            df['altim'] = [int(tree.altim.text[2:6])]
    df.index = df.station_id
    return df

