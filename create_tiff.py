from osgeo import gdal
from osgeo import osr
from remap import remap


def create_tiff(filename, output, bbox):
    # config
    GDAL_DATA_TYPE = gdal.GDT_Float64 
    GEOTIFF_DRIVER_NAME = 'GTiff'
    SPATIAL_REFERENCE_SYSTEM_WKID = 4326
    BBOX = bbox
    FILE = filename

    data = remap(FILE, BBOX, 2, 'NETCDF').ReadAsArray()
    
    xres = abs(BBOX[0]-BBOX[2]) / data.shape[1]
    yres = abs(BBOX[1]-BBOX[3]) / data.shape[0]
    
    geotransform = (BBOX[0], xres, 0, BBOX[3], 0, -yres)
    
    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName(GEOTIFF_DRIVER_NAME)\
    .Create(output, data.shape[1], data.shape[0], 1, GDAL_DATA_TYPE)
    
    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(SPATIAL_REFERENCE_SYSTEM_WKID) 
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(data)   # write a-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None
    
    print(output, 'created')        

if __name__ == "__main__":
    BBOX = [-53.08059692, -25.25489044, -44.20065689, -19.78015137]
    FILE = "OR_ABI-L2-CMIPF-M3C13_G17_s20190010030381_e20190010041159_c20190010041214.nc"
    OUTPUT = "raster_sp.tiff"
    
    create_tiff(FILE, OUTPUT, BBOX)