
#This script is used to change the data format
import gdal
import numpy as np
import os


command = 'gdal_translate -ot float32 -of VRT -co COMPRESS=deflate -unscale -a_nodata \
    -32767.0 -a_srs EPSG:4326  NETCDF:"input_file":sst output_file'
os.system(command)
command2 = 'gdalwarp -of GTIFF input_file output_file'
os.system(command2)
