import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import Point
import cartopy.io.img_tiles as cimgt

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


extent = [-107.5, -89.85, 30.6, 41.15]

request = cimgt.OSM()

# fig = plt.figure(figsize=(8, 5))
# ax = plt.axes(projection=ccrs.Mercator())#request.crs)
#
#
# ax.set_extent(extent)
#
# ax.add_image(request, 6, interpolation='bilinear')
#
quakes_df = pd.read_csv('../data/okQuakes.csv', parse_dates=['time'])
crs = {'init' : 'epsg:4326'}
geometry = [Point(Lat, Lon) for Lat, Lon in zip(quakes_df['longitude'], quakes_df['latitude'])]

quakes_shp = gpd.GeoDataFrame(quakes_df, crs = crs, geometry = geometry)

# plt.close()
# fig.savefig('./test2.png', bbox_inches='tight')
# # extent = [-107.5, -89.85, 30.6, 41.15]
# #
#
# fig = plt.figure(figsize=(8, 5))
# ax = plt.axes(projection=request.crs)#request.crs)
#
# ax.set_extent(extent)
# ax.add_image(request, 6, interpolation='bilinear')
#
# ax.set_xlim(-107.5, -89.85)
# ax.set_ylim(30.6, 41.15)
#

for year in range(1973, 2017):
    fig = plt.figure(figsize=(8, 5))
    ax = plt.axes(projection=request.crs)#request.crs)

    ax.set_extent(extent)
    ax.add_image(request, 6, interpolation='bilinear')

    # ax.set_xlim(-107.5, -89.85)
    # ax.set_ylim(30.6, 41.15)

    mag = quakes_shp.loc[quakes_shp['time'].dt.year == year, 'mag']
    quakes_shp[quakes_shp['time'].dt.year == year].plot(ax = ax, markersize = mag * 10, transform = ccrs.Geodetic())

    ax.set_title(year)
    plt.tight_layout()
    plt.close()
    fig.savefig('../figs/giff/Ok_quakes_{}.png'.format(year), dpi = 400, bbox_inches='tight')
