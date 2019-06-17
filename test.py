from metar_parse import parse_metar
from metpy.units import units
from process_stations import StationLookup
import numpy as np

master = StationLookup().sources[0][1]
for station in StationLookup().sources:
    master = {**master, **station[1]}

def test1():
    df = parse_metar("KATL 102052Z 31008KT 10SM FEW013 SCT100 BKN150 BKN250 26/22 A2996"
                     "RMK AO2 SLP136 VIRGA NW-N TCU DSNT NE 60001 T02610222 58006", master, True)
    assert df.station_id.values == "KATL"
    assert df.temperature.values == 26
    assert df.dewpoint.values == 22
    assert df.altimeter.values == 29.96
    assert df.wind_direction.values == 310
    assert df.wind_speed.values == 8

def test2():
    df = parse_metar("KBOS 102054Z 11015KT 10SM FEW031 FEW090 SCT160 SCT200 BKN280 22/15 A3007 "
                     "RMK AO2 SLP181 T02170150 57024", master, True)
    assert df.skyc1.values == "FEW"
    assert df.skylev1.values == 3100
    assert df.skyc2.values == "FEW"
    assert df.skylev2.values == 9000
    assert df.skyc3.values == "SCT"
    assert df.skylev3.values == 16000
    assert df.skyc4.values == "SCT"
    assert df.skylev4.values == 20000

def test3():
    df = parse_metar("KJFK 102151Z 12008KT 1/4SM R04R/2800V4000FT BR OVC002 19/19 A2995 "
                     "RMK AO2 SFC VIS 3 SLP143 VIS E-SE 1 1/2 T01940194 $", master, True)
    assert df.temperature.values == 19
    assert df.dewpoint.values == 19
    assert df.altimeter.values == 29.95
    assert df.sea_level_pressure.values == 1014

def test4():
    df = parse_metar("KLAS 102156Z VRB03KT 10SM BKN250 34/M06 A3007 RMK AO2 SLP154 T03441061", master, True)
    np.testing.assert_equal(df.wind_direction.values, np.nan)
    assert df.wind_speed.values == 3
    assert df.sea_level_pressure.values == 1013
    assert df.dewpoint.values == -6

def test5():
    df = parse_metar("METAR KFOE 131345Z 11008KT 1 1/2SM BR-DZ OVC013 00/M02 A3049", master, True)
    assert df.wx1.values == "BR-DZ"
    assert df.temperature.values == 00

def test6():
    df = parse_metar("KABQ 042352Z 29013KT 10SM FEW035 BKN065 BKN090 10/02 A2991 RMK AO2 "
                "PK WND 20029/2253 WSHFT 2318 RAE08 SLPNO VIRGA S MTNS OBSC NE-SE "
                "P0001 60014 T01000022 10144 20089 53014", master, True)
    assert df.temperature.values == 10
def test7():
    df = parse_metar("METAR CYYT 081100Z 00000KT 0SM FG VV000 07/07 A3019 RMK F8 SLP224", master, True)
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
