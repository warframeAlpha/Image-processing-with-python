import os
import numpy as np
import time
import rasterio
import gdal
import pandas as pd
from scipy.stats import lognorm
# This program uses gdal_translate to subset muiltiple images. 
# For each image, this program generate several tiles with overlap areas.
# data = gdal.Open("E:/t100/t_max_mask_subset.tif")
# E:/t100/regression/c_scipy.dat
# print(data.RasterXSize,data.RasterYSize)
command = "gdalinfo E:/t100/t_max_mask_subset.tif"
# os.system(command)
ulx="199634.993"
uly='2879208.673'
lrx =  '444054.069'
lry='2655769.775'
# command2="gdal_translate -of ENVI -b 1 -projwin 199634.993 2879208.673 444054.069 2655769.775 E:/t100/ss_max_mask.tif E:/t100/ss_max_mask.tiff"
# os.system(command2)
# print(np.nan+1)

# read results from different methods and read the original data

tmax = gdal.Open("E:/t100/t_max_mask_subset.tif")
tmax = tmax.GetRasterBand(1).ReadAsArray()
# print(np.max(tmax))
# print(np.min(tmax))
# print(tmax[154][266])

a = np.nan
a=1
print(a)