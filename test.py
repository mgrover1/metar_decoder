from metar_parse import parse_metar
import numpy as np

def test1():
    df = parse_metar("KATL 102052Z 31008KT 10SM FEW013 SCT100 BKN150 BKN250 26/22 A2996"
                     "RMK AO2 SLP136 VIRGA NW-N TCU DSNT NE 60001 T02610222 58006")
    assert df.station_id.values == "KATL"
    assert df.temp.values == 26
    assert df.dewp.values == 22
    assert df.altim.values == 1014
    assert df.wind_dir.values == 310
    assert df.wind_spd.values == 8

def test2():
    df = parse_metar("KBOS 102054Z 11015KT 10SM FEW031 FEW090 SCT160 SCT200 BKN280 22/15 A3007 "
                     "RMK AO2 SLP181 T02170150 57024")
    assert df.skyc1.values == "FEW"
    assert df.skylev1.values == 3100
    assert df.skyc2.values == "FEW"
    assert df.skylev2.values == 9000
    assert df.skyc3.values == "SCT"
    assert df.skylev3.values == 16000
    assert df.skyc4.values == "SCT"
    assert df.skylev4.values == 20000
    assert df.temp.values == 22
    assert df.dewp.values == 15

def test3():
    df = parse_metar("KJFK 102151Z 12008KT 1/4SM R04R/2800V4000FT BR OVC002 19/19 A2995 "
                     "RMK AO2 SFC VIS 3 SLP143 VIS E-SE 1 1/2 T01940194 $")
    assert df.temp.values == 19
    assert df.dewp.values == 19
    assert df.altim.values == 1014
    assert df.wind_dir.values == 120
    assert df.wind_spd.values == 8

def test4():
    df = parse_metar("KLAS 102156Z VRB03KT 10SM BKN250 34/M06 A3007 RMK AO2 SLP154 T03441061")
    np.testing.assert_equal(df.wind_dir.values, np.nan)
    assert df.wind_spd.values == 3
    assert df.altim.values == 1018
    assert df.dewp.values == -6

def test5():
    df = parse_metar("METAR KFOE 131345Z 11008KT 1 1/2SM BR-DZ OVC013 00/M02 A3049")
    assert df.wx1.values == "BR-DZ"
    assert df.temp.values == 00

def test6():
    df = parse_metar("KABQ 042352Z 29013KT 10SM FEW035 BKN065 BKN090 10/02 A2991 RMK AO2 "
                "PK WND 20029/2253 WSHFT 2318 RAE08 SLPNO VIRGA S MTNS OBSC NE-SE "
                "P0001 60014 T01000022 10144 20089 53014")
    assert df.temp.values == 10
def test7():
    df = parse_metar("METAR CYYT 081100Z 00000KT 0SM FG VV000 07/07 A3019 RMK F8 SLP224")
    assert df.wx1.values == 'FG'
    assert df.skyc1.values == 'VV'
    assert df.cloudcover.values == 8

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    print("Everything Passed")