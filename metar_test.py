def test1(decoded_metar):
    """ Tests to see if the METAR parser is decoding correctly

    decoded metar should be the dataframe created after parsing the METAR
    """
    import pandas as pd

    df = decoded_metar

    #Checks station ID
    assert df.station_id == 'KFOE'

    #Checks the day
    assert df.  == 13

    #Checks time
    assert df.time == 1345

    #Checks wind direction
    assert df.wind_dir == 110

    #Checks wind speed
    assert df.wind_sped == 8

    #Checks weather 1
    assert df.wx1 == 'BR'

    #Checks weather 2
    assert df.wx2 == '-DZ'

    #Checks skyc1
    assert df.skyc1 == 'OVC013'

    #Checks skyc2
    assert df.skyc2 == pd.NaT

    #Checks skyc3
    assert df.skyc3 == pd.NaT

    #Checks temperature
    assert df.temp == 0

    #Checks dewpoint
    assert df.dewp == -2

    #Checks altimeter
    assert df.altim == 30.49

def test2(decoded_metar)
