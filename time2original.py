
# This file is used to compute how long each pixel takes to their original state
## read images
import numpy as np
from scipy.optimize import fsolve
import os
import shutil
import matplotlib.pyplot as plt
import gdal
driver = gdal.GetDriverByName('GTIFF')
## read images
img_matrix = gdal.Open("E:/t100/regression/img_matrix_subset.dat")
geot = img_matrix.GetGeoTransform()
proj = img_matrix.GetProjection()
img_matrix = img_matrix.ReadAsArray() 
print(img_matrix.shape)
## read a b c (regression result)
abc = gdal.Open("E:/t100/regression/coefficients_gmodel_powell.tiff")
a = abc.GetRasterBand(1).ReadAsArray()
b = abc.GetRasterBand(2).ReadAsArray()
c = abc.GetRasterBand(3).ReadAsArray()
print(c.shape)
[col,row]=[abc.RasterXSize,abc.RasterYSize]
abc = None
## read 4-days mean image
init_state = gdal.Open('E:/t100/DecayData_Chau/04_07_mean_subset.tiff')
init_state = init_state.ReadAsArray()
print(init_state.shape)
## read SS max and tmax
ss_max = gdal.Open("E:/t100/ss_max_mask.tiff")
ss_max = ss_max.ReadAsArray()
print(ss_max.shape)
t_max = gdal.Open("E:/t100/t_max_mask_subset.tif")
t_max = t_max.GetRasterBand(1).ReadAsArray()
print(t_max.shape)
## def max variation
SSa = ss_max-init_state
t_matrix = []
for i in range(19):
    for j in range(8):
        if i != 4 and i!= 5 and i!= 6 and i!=11 and i!= 12 and i!= 13 and i != 14:
            t_matrix.append(24*i+j)
###
def f(t,p):
    a=p[0]
    b=p[1]
    c = p[2]
    threshold = p[3]
    tmaxx = p[4]
    return a*np.exp(-b*(t-tmaxx))+c-threshold
## Now we choose compute_t4

def image_stactistic(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_min = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_min = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    max_avg = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))

    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            
            indexx = np.argmax(img_matrix[i][j])
            t_max[i][j] = t_matrix[indexx]
            ss_max[i][j] = img_matrix[i][j][indexx]
# to avoid seize no data as t_min and ss_min
            img_temp = []
            t_temp = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k] !=0:
                    img_temp.append(img_matrix[i][j][k])
                    t_temp.append(t_matrix[k])
            if len(img_temp)>0:
                indexy = np.argmin(img_temp)
                t_min[i][j] = t_temp[indexy] + 8.5 # because GOCI start from 8:30, but the time start from 0. As for t_max, I use seadas to change that
                ss_min[i][j] = img_temp[indexy]
########################################################
            # max_avg[i][j] = ss_max[i][j]- init_state[i][j]

def compute_t4(a,b,c,img_matrix,t_matrix,init_state):
    # this function is used to fullfish Prof. Wang's request (20190905)
    k1 = 0.1 # the only varibale to adjust
    k2 = 1-k1 # t90: k2 = 0.9
    t_method = np.full((row,col),-1)
    for i in range(img_matrix.shape[1]):
        for j in range(img_matrix.shape[2]):
            threshold = k1*ss_max[i][j] + k2*init_state[i][j]
            # threshold = 2.6
            t0 = -1
            if c[i][j]> 0 and a[i][j]>0 and threshold>c[i][j]:
                t0 = fsolve(f,0,[a[i][j],b[i][j],c[i][j],threshold,t_max[i][j]])
                t_method[i][j] = t0
            if t0 <=t_max[i][j]:
                t_method[i][j] = -1
    
    t90 = driver.Create("E:/t100/regression/t90_powell.tiff", xsize = col, ysize = row, bands=1,eType = gdal.GDT_Float32)
    t90.GetRasterBand(1).WriteArray(t_method)
    t90.SetGeoTransform(geot)
    t90.SetProjection(proj)
    print(t90.ReadAsArray().shape)
    t90_after_tmax = driver.Create("E:/t100/regression/t90_powell_after_tmax.tiff", xsize = col, ysize = row, bands=1,eType = gdal.GDT_Float32)
    tt = t_method.copy()
    t_max[tt==-1]=np.nan
    arr = t_method+t_max
    np.nan_to_num(arr,copy=False,nan=-1)
    t90_after_tmax.GetRasterBand(1).WriteArray(arr)
    t90_after_tmax.SetGeoTransform(geot)
    t90_after_tmax.SetProjection(proj)
compute_t4(a,b,c,img_matrix,t_matrix,init_state)
# image_stactistic(a,b,c,img_matrix,t_matrix,init_state)