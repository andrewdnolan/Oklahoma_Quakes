import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
from shapely.geometry import Point


quakes_df = pd.read_csv('../data/okQuakes.csv', parse_dates=['time'])
crs = {'init' : 'epsg:4326'}
geometry = [Point(Lat, Lon) for Lat, Lon in zip(quakes_df['longitude'], quakes_df['latitude'])]

quakes_shp = gpd.GeoDataFrame(quakes_df, crs = crs, geometry = geometry)


for year in range(1973, 2017):

    fig, ax = plt.subplots(1)
    ax.set_xlim(-107.54225322580646, -89.849746774193534)
    ax.set_ylim(30.587871428571429, 41.148128571428572)
    mag = quakes_shp.loc[quakes_shp['time'].dt.year == year, 'mag']
    quakes_shp[quakes_shp['time'].dt.year == year].plot(ax = ax, markersize = mag * 10)

    ax.set_title(year)
    plt.tight_layout()
    fig.savefig('../figs/giff/Ok_quakes_{}.png'.format(year), )
    plt.close()

plt.show()
