#Import the neccessary libraries
from siphon.catalog import TDSCatalog
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from metar_decode import parse
from metar_parse import parse_metar
from process_stations import StationLookup
from altimeter_slp_conversion import altimeter_to_slp
import xarray as xr
import metpy.calc as mpcalc
from metpy.calc import wind_components
from metpy.cbook import get_test_data
from metpy.plots import (add_metpy_logo, simple_layout, StationPlot,
                         StationPlotLayout, wx_code_map)
from metpy.units import units
from datetime import datetime, timedelta
import numpy as np

df = xr.open_dataset("Surface_METAR_20190612_0000.nc", decode_times=True)
reports = df.get("report").values

master = StationLookup().sources[0][1]
for station in StationLookup().sources:
    master = {**master, **station[1]}


print(len(reports))
station_id = []
lat = []
lon = []
elev = []
date_time = []
day =[]
time_utc = []
wind_dir = []
wind_spd = []
wx1 = []
wx2 = []
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
slp = []
unparsed_metars = []
start = datetime.now()
for report in reports:
    try:
        ob = parse_metar(report.decode('utf-8'), master, create_df = False)
        station_id.append(ob[0])
        lat.append(ob[1])
        lon.append(ob[2])
        elev.append(ob[3])
        date_time.append(ob[4])
        day.append(ob[5])
        time_utc.append(ob[6])
        wind_dir.append(ob[7])
        wind_spd.append(ob[8])
        wx1.append(ob[9])
        wx2.append(ob[10])
        skyc1.append(ob[11])
        skylev1.append(ob[12])
        skyc2.append(ob[13])
        skylev2.append(ob[14])
        skyc3.append(ob[15])
        skylev3.append(ob[16])
        skyc4.append(ob[17])
        skylev4.append(ob[18])
        cloudcover.append(ob[19])
        temp.append(ob[20])
        dewp.append(ob[21])
        altim.append(ob[22])
        slp.append(ob[23])

    except:
        None
