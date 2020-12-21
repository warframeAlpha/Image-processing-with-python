import gdal
import numpy as np
import os
def count(img,numm):
    temp_img = img
    temp_img[temp_img>0] = 1
    numm = numm + temp_img
    return numm
example = 'E:/t100/DecayData_Chau/daily_SS/20150812/20150812_0_SS.img'

s = gdal.Open(example)
[col,row] = [s.RasterXSize,s.RasterYSize]
geoj = s.GetGeoTransform()
proj = s.GetProjection()
s = None
print(col,row)
summ = np.zeros((row,col))
numm = np.zeros((row,col))
folder = 'E:/t100/DecayData_Chau/4_days'
os.chdir(folder)
sub_folder = os.listdir(folder)
for sub in sub_folder:
    flist = os.listdir(sub)
    for f in flist:
        if f.endswith('.img'):
            fpath = folder+'/'+sub+'/'+f
            # fpath = os.path.abspath(f)
            # fpath = fpath.replace(os.sep,'/')
            print(fpath)
            data=gdal.Open(fpath)
            img = data.ReadAsArray()
            summ = summ + img
            numm = count(img,numm)
average_array = summ/numm
driver = gdal.GetDriverByName("GTIFF")
average_img = driver.Create('E:/t100/DecayData_Chau/04_07_mean.tiff',col,row,bands=1,eType = gdal.GDT_Float32) 
average_img.GetRasterBand(1).WriteArray(average_array)
average_img.SetGeoTransform(geoj)
average_img.SetProjection(proj)
# num_img = driver.Create('E:/t100/DecayData_Chau/19_22_num.tiff',col,row,bands=1,eType = gdal.GDT_Float32)
# num_img.GetRasterBand(1).WriteArray(numm)
