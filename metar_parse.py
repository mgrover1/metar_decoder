def parse_metar(metar_text, station_dict, create_df):
    """Takes in a metar file, in a text form, and creates a pandas
    dataframe that can be easily subset

    Input:
    metar_text = string with the METAR data
    create_df = True or False
        True creates a Pandas dataframe as the Output
        False creates a list of lists containing the values in the following order:

        [station_id, latitude, longitude, elevation, date_time, day, time_utc,
        wind_direction, wind_speed, wxsymbol1, wxsymbol2, skycover1, skylevel1,
        skycover2, skylevel2, skycover3, skylevel3, skycover4, skylevel4,
        cloudcover, temperature, dewpoint, altimeter_value, sea_level_pressure]

    Output:
    Pandas Dataframe that can be subset easily
    """

    # Import the neccessary libraries
    import pandas as pd
    import numpy as np
    from metar_decode import parse
    from metpy.units import units
    from process_stations import StationLookup
    from calculations import altimeter_to_slp
    import warnings
    warnings.filterwarnings('ignore', 'Pandas doesn\'t allow columns to be created', UserWarning)

    #Create lists for each of the variables
    station_id, lat, lon, elev, date_time, day, time_utc, wind_dir, wind_spd, wx1, wx2, \
    skyc1, skylev1, skyc2, skylev2, skyc3, skylev3, skyc4, skylev4, cloudcover, temp, dewp, \
    altim, wx1_wmo, wx2_wmo = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

    #Create a dictionary with all the station metadata
    master = station_dict
    #master = StationLookup().sources[0][1]
    #for station in StationLookup().sources:
    #    master = {**master, **station[1]}
    wx_code_map = {'': 0, 'M': 0, 'TSNO': 0, 'VA': 4, 'FU': 4,
                   'HZ': 5, 'DU': 6, 'BLDU': 7, 'SA': 7,
                   'BLSA': 7, 'VCBLSA': 7, 'VCBLDU': 7, 'BLPY': 7,
                   'PO': 8, 'VCPO': 8, 'VCDS': 9, 'VCSS': 9,
                   'BR': 10, 'BCBR': 10, 'BC': 11, 'MIFG': 12,
                   'VCTS': 13, 'VIRGA': 14, 'VCSH': 16, 'TS': 17,
                   'THDR': 17, 'VCTSHZ': 17, 'TSFZFG': 17, 'TSBR': 17,
                   'TSDZ': 17, 'SQ': 18, 'FC': 19, '+FC': 19,
                   'DS': 31, 'SS': 31, 'DRSA': 31, 'DRDU': 31,
                   'TSUP': 32, '+DS': 34, '+SS': 34, '-BLSN': 36,
                   'BLSN': 36, '+BLSN': 36, 'VCBLSN': 36, 'DRSN': 38,
                   '+DRSN': 38, 'VCFG': 40, 'BCFG': 41, 'PRFG': 44,
                   'FG': 45, 'FZFG': 49, '-VCTSDZ': 51, '-DZ': 51,
                   '-DZBR': 51, 'VCTSDZ': 53, 'DZ': 53, '+VCTSDZ': 55,
                   '+DZ': 55, '-FZDZ': 56, '-FZDZSN': 56, 'FZDZ': 57,
                   '+FZDZ': 57, 'FZDZSN': 57, '-DZRA': 58, 'DZRA': 59,
                   '+DZRA': 59, '-VCTSRA': 61, '-RA': 61, '-RABR': 61,
                   'VCTSRA': 63, 'RA': 63, 'RABR': 63, 'RAFG': 63,
                   '+VCTSRA': 65, '+RA': 65, '-FZRA': 66, '-FZRASN': 66,
                   '-FZRABR': 66, '-FZRAPL': 66, '-FZRASNPL': 66, 'TSFZRAPL': 67,
                   '-TSFZRA': 67, 'FZRA': 67, '+FZRA': 67, 'FZRASN': 67,
                   'TSFZRA': 67, '-DZSN': 68, '-RASN': 68, '-SNRA': 68,
                   '-SNDZ': 68, 'RASN': 69, '+RASN': 69, 'SNRA': 69,
                   'DZSN': 69, 'SNDZ': 69, '+DZSN': 69, '+SNDZ': 69,
                   '-VCTSSN': 71, '-SN': 71, '-SNBR': 71, 'VCTSSN': 73,
                   'SN': 73, '+VCTSSN': 75, '+SN': 75, 'VCTSUP': 76,
                   'IN': 76, '-UP': 76, 'UP': 76, '+UP': 76,
                   '-SNSG': 77, 'SG': 77, '-SG': 77, 'IC': 78,
                   '-FZDZPL': 79, '-FZDZPLSN': 79, 'FZDZPL': 79, '-FZRAPLSN': 79,
                   'FZRAPL': 79, '+FZRAPL': 79, '-RAPL': 79, '-RASNPL': 79,
                   '-RAPLSN': 79, '+RAPL': 79, 'RAPL': 79, '-SNPL': 79,
                   'SNPL': 79, '-PL': 79, 'PL': 79, '-PLSN': 79,
                   '-PLRA': 79, 'PLRA': 79, '-PLDZ': 79, '+PL': 79,
                   'PLSN': 79, 'PLUP': 79, '+PLSN': 79, '-SH': 80,
                   '-SHRA': 80, 'SH': 81, 'SHRA': 81, '+SH': 81,
                   '+SHRA': 81, '-SHRASN': 83, '-SHSNRA': 83, '+SHRABR': 84,
                   'SHRASN': 84, '+SHRASN': 84, 'SHSNRA': 84, '+SHSNRA': 84,
                   '-SHSN': 85, 'SHSN': 86, '+SHSN': 86, '-GS': 87,
                   '-SHGS': 87, 'FZRAPLGS': 88, '-SNGS': 88, 'GSPLSN': 88,
                   'GSPL': 88, 'PLGSSN': 88, 'GS': 88, 'SHGS': 88,
                   '+GS': 88, '+SHGS': 88, '-GR': 89, '-SHGR': 89,
                   '-SNGR': 90, 'GR': 90, 'SHGR': 90, '+GR': 90,
                   '+SHGR': 90, '-TSRA': 95, 'TSRA': 95, 'TSSN': 95,
                   'TSPL': 95, '-TSDZ': 95, '-TSSN': 95, '-TSPL': 95,
                   'TSPLSN': 95, 'TSSNPL': 95, '-TSSNPL': 95, 'TSRAGS': 96,
                   'TSGS': 96, 'TSGR': 96, '+TSRA': 97, '+TSSN': 97,
                   '+TSPL': 97, '+TSPLSN': 97, 'TSSA': 98, 'TSDS': 98,
                   'TSDU': 98, '+TSGS': 99, '+TSGR': 99}
    # Decode the data using the parser (built using Canopy)
    tree = parse(metar_text)

    #Station ID, Latitude, Longitude, and Elevation
    if tree.siteid.text == '':
        station_id.append(np.nan)
    else:
        station_id.append(tree.siteid.text.strip())
        #Extract the latitude and longitude values from "master" dictionary
        try:
            lat.append(master[tree.siteid.text.strip()].latitude)
            lon.append(master[tree.siteid.text.strip()].longitude)
            elev.append(master[tree.siteid.text.strip()].altitude)
        except:
            lat.append(np.nan)
            lon.append(np.nan)
            elev.append(np.nan)

    # Set the datetime, day, and time_utc
    if tree.datetime.text == '':
        datetime.append(np.nan)
        day.append(np.nan)
        time_utc.append(np.nan)
    else:
        datetime = tree.datetime.text[:-1].strip()
        date_time.append(datetime)
        day.append(datetime[0:2])
        time_utc.append(datetime[2:7])

    # Set the wind variables
    if tree.wind.text == '':
        wind_dir.append(np.nan)
        wind_spd.append(np.nan)
    elif (tree.wind.text == '/////KT') or (tree.wind.text ==' /////KT') or (tree.wind.text == 'KT'):
        wind_dir.append(np.nan)
        wind_spd.append(np.nan)
    else:
        if (tree.wind.wind_dir.text == 'VRB') or (tree.wind.wind_dir.text == 'VAR'):
            wind_dir.append(np.nan)
            wind_spd.append(float(tree.wind.wind_spd.text))
        else:
            wind_dir.append(int(tree.wind.wind_dir.text))
            wind_spd.append(int(tree.wind.wind_spd.text))

    # Set the weather symbols
    if tree.curwx.text == '':
        wx1.append(np.nan)
        wx2.append(np.nan)
        wx1_wmo.append(np.nan)
        wx2_wmo.append(np.nan)
    else:
        wx = [np.nan, np.nan]
        wx[0:len((tree.curwx.text.strip()).split())] = tree.curwx.text.strip().split()
        wx1.append(wx[0])
        wx2.append(wx[1])
        try:
            wx1_wmo.append(int(wx_code_map[wx[0]]))
        except:
            wx1_wmo.append(np.nan)
        try:
            wx2_wmo.append(int(wx_code_map[wx[1]]))
        except:
            wx2_wmo.append(np.nan)

    # Set the sky conditions

    if tree.skyc.text == '':
        skyc1.append(np.nan)
        skylev1.append(np.nan)
        skyc2.append(np.nan)
        skylev2.append(np.nan)
        skyc3.append(np.nan)
        skylev3.append(np.nan)
        skyc4.append(np.nan)
        skylev4.append(np.nan)

    elif tree.skyc.text[1:3] == 'VV':
        skyc1.append('VV')
        skylev1.append(tree.skyc.text.strip()[2:])
        skyc2.append(np.nan)
        skylev2.append(np.nan)
        skyc3.append(np.nan)
        skylev3.append(np.nan)
        skyc4.append(np.nan)
        skylev4.append(np.nan)

    else:
        skyc = [np.nan, np.nan, np.nan, np.nan]
        skyc[0:len((tree.skyc.text.strip()).split())] = tree.skyc.text.strip().split()
        try:
            skyc1.append(skyc[0][0:3])
            skylev1.append((float(skyc[0][3:])*100))

        except:
            skyc1.append(np.nan)
            skylev1.append(np.nan)
        try:
            skyc2.append(skyc[1][0:3])
            skylev2.append((float(skyc[1][3:])*100))
        except:
            skyc2.append(np.nan)
            skylev2.append(np.nan)
        try:
            skyc3.append(skyc[2][0:3])
            skylev3.append((float(skyc[2][3:])*100))
        except:
            skyc3.append(np.nan)
            skylev3.append(np.nan)
        try:
            skyc4.append(skyc[3][0:3])
            skylev4.append((float(skyc[3][3:])*100))
        except:
            skyc4.append(np.nan)
            skylev4.append(np.nan)

    if skyc1[0] == ('SKC' or 'NCD' or 'NSC' or 'CLR'):
        cloudcover.append(0)
    elif skyc1[0] == 'FEW':
        cloudcover.append(2)
    elif skyc1[0] == 'SCT':
        cloudcover.append(4)
    elif skyc1[0] == 'BKN':
        cloudcover.append(6)
    elif skyc1[0] == ('OVC' or 'VV'):
        cloudcover.append(8)
    else:
        cloudcover.append(np.nan)

    # Set the temperature and dewpoint
    if (tree.temp_dewp.text == '') or (tree.temp_dewp.text == ' MM/MM'):
        temp.append(np.nan)
        dewp.append(np.nan)
    else:
        try:
            if "M" in tree.temp_dewp.temp.text:
                temp.append(-1 * float(tree.temp_dewp.temp.text[-2:]))
            else:
                temp.append(float(tree.temp_dewp.temp.text[-2:]))
        except:
            temp.append(np.nan)
        try:
            if "M" in tree.temp_dewp.dewp.text:
                dewp.append(-1 * float(tree.temp_dewp.dewp.text[-2:]))
            else:
                dewp.append(float(tree.temp_dewp.dewp.text[-2:]))
        except:
            dewp.append(np.nan)

    # Set the altimeter value and sea level pressure
    if tree.altim.text == '':
        altim.append(np.nan)
        #slp.append(np.nan)
    else:
        if (float(tree.altim.text.strip()[1:5])) > 1100:
            altim.append(float(tree.altim.text.strip()[1:5]) / 100)
        else:
            altim.append((int(tree.altim.text.strip()[1:5])*units.hPa).to('inHg').magnitude)
        #try:
            #slp.append(int(altimeter_to_slp(
            #altim[0]*units('inHg'),
            #elev[0]*units('meters'),
            #temp[0]*units('degC')).magnitude))
        #except:
            #slp.append(np.nan)

    if create_df == True:
        col_units = {
        'station_id': None,
        'lat': 'degrees',
        'lon': 'degrees',
        'elev': 'meters',
        'date_time': None,
        'day': None,
        'time_utc': None,
        'wind_dir': 'degrees',
        'wind_spd': 'kts',
        'wx1': None,
        'wx2': None,
        'skyc1': None,
        'skylev1': 'feet',
        'skyc2': None,
        'skylev2': 'feet',
        'skyc3': None,
        'skylev3': 'feet',
        'skyc4': None,
        'skylev4:': None,
        'cloudcover': None,
        'temp': 'degC',
        'dewp': 'degC',
        'altim': 'inHg'}
        #'slp': 'hPa'}

        df = pd.DataFrame({'station_id':station_id, 'latitude':lat,
        'longitude':lon, 'elevation':elev,
        'date_time':date_time, 'day':day,
        'time_utc':time_utc, 'wind_direction':wind_dir,
        'wind_speed':wind_spd,'wx1':wx1, 'wx2':wx2,
        'skyc1':skyc1, 'skylev1':skylev1,
        'skyc2':skyc2, 'skylev2':skylev2, 'skyc3':skyc3,
        'skylev3': skylev3, 'skyc4':skyc4, 'skylev4':skylev4,
        'cloudcover':cloudcover, 'temperature':temp, 'dewpoint':dewp,
        'altimeter':altim, 'wx_symbol1_wmo':wx1_wmo, 'wx_symbol2_wmo':wx2_wmo})
        try:
            df['sea_level_pressure'] = float(format(altimeter_to_slp(
            altim[0]*units('inHg'),
            elev[0]*units('meters'),
            temp[0]*units('degC')).magnitude, '.1f'))
        except:
            df['slp'] = [np.nan]
        df.units = col_units
        df.index = df.station_id
        df['altimeter'] = df.altimeter.round(2)
        df['sea_level_pressure'] = df.sea_level_pressure.round(2)
        return df
    else:
        ob = [station_id, lat, lon, elev, date_time, day, time_utc, wind_dir, wind_spd, wx1, wx2,
        skyc1, skylev1, skyc2, skylev2, skyc3, skylev3, skyc4, skylev4, cloudcover, temp, dewp, altim,
        wx1_wmo, wx2_wmo]
        return ob
