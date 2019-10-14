import os
from osgeo import gdal
from osgeo import osr
import numpy as np
from remap import remap
from netCDF4 import Dataset

# config
GDAL_DATA_TYPE = gdal.GDT_Float64 
GEOTIFF_DRIVER_NAME = 'GTiff'
NO_DATA = 15
SPATIAL_REFERENCE_SYSTEM_WKID = 4326
BBOX = [-53.08059692, -25.25489044, -44.20065689, -19.78015137]
FILE = "OR_ABI-L2-CMIPF-M3C13_G17_s20190010030381_e20190010041159_c20190010041214.nc"

nc = Dataset(FILE, 'r')
data = remap(FILE, BBOX, 2, 'NETCDF').ReadAsArray()

xres = abs(BBOX[0]-BBOX[2]) / data.shape[1]
yres = abs(BBOX[1]-BBOX[3]) / data.shape[0]

geotransform = (BBOX[0], xres, 0, BBOX[3], 0, -yres)

# create the 3-band raster file
dst_ds = gdal.GetDriverByName('GTiff').Create('sao_paulo.tiff', data.shape[1], data.shape[0], 1, gdal.GDT_Float64)

dst_ds.SetGeoTransform(geotransform)    # specify coords
srs = osr.SpatialReference()            # establish encoding
srs.ImportFromEPSG(4326)                # WGS84 lat/long
dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
dst_ds.GetRasterBand(1).WriteArray(data)   # write a-band to the raster
dst_ds.FlushCache()                     # write to disk
dst_ds = None
    
