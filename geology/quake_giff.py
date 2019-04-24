import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import Point
import cartopy.io.img_tiles as cimgt
import matplotlib.gridspec as gridspec

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


extent = [-110, -84, 30.6, 41.15] #[-107.5, -89.85, 30.6, 41.15] #

request = cimgt.OSM()

quakes_df = pd.read_csv('../data/okQuakes.csv', parse_dates=['time'])

counts_per_year = quakes_df.loc[quakes_df['mag'] > 3.0].groupby(quakes_df['time'].dt.year).count()

crs = {'init' : 'epsg:4326'}
geometry = [Point(Lat, Lon) for Lat, Lon in zip(quakes_df['longitude'], quakes_df['latitude'])]
quakes_shp = gpd.GeoDataFrame(quakes_df, crs = crs, geometry = geometry)


gs = gridspec.GridSpec(2, 1, height_ratios=(3,1))

for year in range(1973, 2017):
    fig = plt.figure(figsize=(8,6))

    ax = plt.axes(projection=request.crs)#request.crs)

    ax0 = plt.subplot(gs[0:1, 0], projection=request.crs)
    ax1 = plt.subplot(gs[1, 0])

    ax0.set_extent(extent)
    ax0.add_image(request, 5, interpolation='spline36')

    # ax.set_xlim(-107.5, -89.85)
    # ax.set_ylim(30.6, 41.15)

    mag = quakes_shp.loc[quakes_shp['time'].dt.year == year, 'mag']
    quakes_shp[quakes_shp['time'].dt.year == year].plot(ax = ax0, markersize = mag * 10, alpha = 0.5, transform = ccrs.Geodetic())

    ax1.bar(counts_per_year.index, counts_per_year['mag'], color = 'grey')
    ax1.bar(year, counts_per_year.loc[year,'mag'])
    ax1.text(year, counts_per_year.loc[year,'mag'] + 100, str(year), size = 8, ha="left", va="center", rotation = 30)

    ax0.set_title(year)
    plt.tight_layout()
    plt.close()
    fig.savefig('../figs/giff/Ok_quakes_{}.png'.format(year), dpi = 400, bbox_inches='tight')
