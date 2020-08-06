import gdal
import numpy as np
import os
data_04_07 = gdal.Open('E:/t100/DecayData_Chau/04_07_mean.tiff')
data_11_14 = gdal.Open('E:/t100/DecayData_Chau/11_14_mean.tiff')
data_19_22 = gdal.Open('E:/t100/DecayData_Chau/19_22_mean.tiff')
num_04_07 = gdal.Open('E:/t100/DecayData_Chau/04_07_num.tiff')
num_11_14 = gdal.Open('E:/t100/DecayData_Chau/11_14_num.tiff')
num_19_22 = gdal.Open('E:/t100/DecayData_Chau/19_22_num.tiff')
img_04_07 = data_04_07.ReadAsArray()
img_11_14 = data_11_14.ReadAsArray()
img_19_22 = data_19_22.ReadAsArray()
num_04_07 = num_04_07.ReadAsArray()
num_11_14 = num_11_14.ReadAsArray()
num_19_22 = num_19_22.ReadAsArray()
[col,row]=[data_04_07.RasterXSize,data_04_07.RasterYSize]

data_04_07=None
data_11_14=None
data_19_22=None
crs = gdal.Open('E:/t100/DecayData_Chau/20150820/20150820_0_SS.img')
geot = crs.GetGeoTransform()
proj = crs.GetProjection()
crs = None
def difference():
    driver = gdal.GetDriverByName('ENVI')
    num_04_07[num_04_07==0]=1
    num_11_14[num_11_14==0]=1
    num_19_22[num_19_22==0]=1
    # 11~14-04~07
    RMSE1 = 2.6/np.sqrt(num_04_07)+2.6/np.sqrt(num_11_14)
    difference_array1 = img_11_14-img_04_07-RMSE1
    # 19~22-04~07

    RMSE2 = 2.6/np.sqrt(num_04_07)+2.6/np.sqrt(num_19_22)
    print(RMSE2)
    difference_array2 = img_19_22 - img_04_07-RMSE2

    # binary result
    difference_array1[difference_array1>0] = 1
    difference_array1[difference_array1<=0] = 0
    difference_array2[difference_array2>0] =1
    difference_array2[difference_array2<=0] =0
    impacted_region1 = driver.Create('E:/t100/DecayData_Chau/impacted_region_11_14.dat',col,row,bands=1,eType = gdal.GDT_Float32)
    impacted_region2 = driver.Create('E:/t100/DecayData_Chau/impacted_region_19_22.dat',col,row,bands=1,eType = gdal.GDT_Float32)
    impacted_region1.GetRasterBand(1).WriteArray(difference_array1)
    impacted_region2.GetRasterBand(1).WriteArray(difference_array2)
    impacted_region1.SetGeoTransform(geot)
    impacted_region1.SetProjection(proj)
    impacted_region2.SetGeoTransform(geot)
    impacted_region2.SetProjection(proj)
difference()