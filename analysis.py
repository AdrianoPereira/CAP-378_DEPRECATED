import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from remap import remap
import geopandas as gpd


file = "data/2017/10/2/OR_ABI-L2-CMIPF-M3C02_G16_s20172750930388_e20172750941155_c20172750941226.nc"

#bbox = [-53.08059692, -25.25489044, -44.20065689, -19.78015137]

shapefile = 'shapes/Brazilian_States_Shape/BRA_adm1.shp'
shp = gpd.read_file(shapefile)
state = shp[shp['ADM1'] == 'SAO PAULO']
bbox = state.bounds.values[0]

grid = remap(file, bbox, 2, 'NETCDF')
data = grid.ReadAsArray()

#DPI = 150
#ax = plt.figure(figsize=(2000/float(DPI), 2000/float(DPI)), frameon=True, dpi=DPI)

bmap = Basemap(projection='merc', llcrnrlon=bbox[0], llcrnrlat=bbox[1], 
               urcrnrlon=bbox[2], urcrnrlat=bbox[3]+0.5, epsg=4326, resolution='i')

bmap.bluemarble()
bmap.imshow(data, cmap='jet', alpha=.8)
bmap.readshapefile(shapefile.split('.')[0], 'states', drawbounds=True, color='#dcdcdc', linewidth=2)
cbar = bmap.colorbar(location='bottom')


bmap.drawmeridians(np.linspace(bbox[0], bbox[2], 5), color='#dcdcdc', 
                   alpha=.2, fmt='%g', labels=[0, 0, 1, 0], )


bmap.drawparallels(np.linspace(bbox[1], bbox[3], 5), color='#dcdcdc', 
                   alpha=.2, fmt='%g', labels=[0, 1, 0, 0])


plt.savefig('plot.png')
plt.show()
