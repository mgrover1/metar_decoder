def parse_metar(metar_text):
    """Takes in a metar file, in a text form, and creates a pandas
    dataframe that can be easily subset

    Input:
    metar_text = string with the METAR data

    Output:
    Pandas Dataframe that can be subset easily
    """

    #Import the neccessary libraries
    import pandas as pd
    import numpy as np
    from metar_decode import parse
    from metpy.units import units

    #Build a dataframe that will store the data
    df = pd.DataFrame()

    #Decode the data using the parser (built using Canopy)
    tree = parse(metar_text)

    #Set the station id
    if tree.siteid.text == '':
        df['station_id'] = np.nan
    else:
        df['station_id'] = tree.siteid.text

    #Set the datetime
    if tree.datetime.text == '':
        df['date_time'] = np.nan
        df['day'] = np.nan
        df['time_utc'] = np.nan
    else:
        datetime = tree.datetime.text[:-1]
        df['date_time'] = datetime
        df['day'] = int(datetime[0:3])
        df['time_utc'] = int(datetime[3:])

    #Set the wind variables
    if tree.wind.text == '':
        df['wind_dir'] = np.nan
        df['wind_spd'] = np.nan
    else:
        if df['wind_dir'] == 'VRB':
            df['wind_dir'] = np.nan
        else:
            df['wind_dir'] = int(tree.wind.wind_spd.text)

    #Set the weather symbols
    if tree.curwx.text == '':
        df['wx1'] = np.nan
        df['wx2'] = np.nan
    else:
        wx = [np.nan, np.nan]
        wx[0:len((tree.curwx.text.strip()).split())] = tree.curwx.text.strip().split()
        df['wx1'] = wx[0]
        df['wx2'] = wx[1]

    #Set the sky conditions
    if tree.skyc.text == '':
        df['skyc1'] = np.nan
        df['skyc2'] = np.nan
        df['skyc3'] = np.nan
    else:
        skyc = [np.nan, np.nan, np.nan]
        skyc[0:len((tree.skyc.text.strip()).split())] = tree.skyc.text.strip().split()
        df['skyc1'] = skyc[0]
        df['skyc2'] = skyc[1]
        df['skyc3'] = skyc[2]

    #Set the temperature and dewpoint
    if tree.temp_dewp.text == '':
        df['temp'] = np.nan
        df['dewp'] = np.nan
    else:
        if "M" in tree.temp_dewp.temp.text:
            df['temp'] = (-1*float(tree.temp_dewp.temp.text[-2:]))
        else:
            df['temp'] = float(tree.temp_dewp.temp.text[-2:])
        if "M" in tree.temp_dewp.dewp.text:
            df['dewp'] = (-1*float(tree.temp_dewp.dewp.text[-2:]))
        else:
            df['dewp'] = float(tree.temp_dewp.dewp.text[-2:])

    #Set the altimeter value
    if tree.altim.text == '':
        df['altim'] = np.nan
    else:
        if (float(tree.altim.text[2:6])) > 1100:
            df['altim'] = (float(tree.altim.text[2:6])/100)*units("inHg").to('hPa').magnitude
        else:
            df['altim'] = float(tree.altim.text[2:6])










