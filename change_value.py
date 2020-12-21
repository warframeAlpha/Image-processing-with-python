import gdal
import numpy
import os
import _thread
import threading, queue
def single_image():
    data = gdal.Open('E:/Deep_frustrating/ENVI_tiles_1250/20161031_Pleiades_HuaDongKao_97_ms_sharpening_masked_subset/20161031_Pleiades_HuaDongKao_97_ms_sharpening_masked_902subset')
    geot = data.GetGeoTransform()
    proj = data.GetProjection()
    img = data.ReadAsArray()
    [col,row] = [data.RasterXSize,data.RasterYSize]
    print(img.shape)
    for b in range(4):
        for i in range(row):
            for j in range(col):
                if img[b][i][j] ==0:
                    img[b][i][j]= 65535
    print('done')
    driver = gdal.GetDriverByName("ENVI")
    fname = 'E:/Deep_frustrating/tiles/902subset_65535'
    new_img = driver.Create(fname,col,row,bands=4,eType = gdal.GDT_Float32)
    new_img.GetRasterBand(1).WriteArray(img[0])
    new_img.GetRasterBand(2).WriteArray(img[1])
    new_img.GetRasterBand(3).WriteArray(img[2])
    new_img.GetRasterBand(4).WriteArray(img[3])
    for i in range(1,5):
        new_img.GetRasterBand(i).SetNoDataValue(65535)    
    data = None
    img = None
    new_img.SetGeoTransform(geot)
    new_img.SetProjection(proj)
def create_fname(path,target_folder):
    fname = ''
    for i in range(path.rfind(r'/'),len(path)):
        fname = fname + path[i]
    fname = target_folder+fname
    return fname
def worker():
    driver = gdal.GetDriverByName('ENVI')
    folder = 'E:/Deep_frustrating/ENVI_tiles_1250'
    sub_folder = os.listdir(folder)
    print(sub_folder)
    for sub in sub_folder:
        q = queue.Queue()
        target_folder = 'E:/Deep_frustrating/ENVI_tiles_1250_65535/'+sub
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        fpath = folder+'/'+sub
        files = os.listdir(fpath)
        for f in files:
            if f.endswith('subset'):
                full_path = fpath+'/'+f
                q.put(full_path)
        for thread_num in range(6):
            _thread.start_new_thread(change_value,(q,target_folder,f,driver,thread_num))
        q.join()
def change_value(q,target_folder,f,driver,c): 
    while q.empty() == False:
        path = q.get(False)
        # print(c)
        data = gdal.Open(path)
        geot = data.GetGeoTransform()
        proj = data.GetProjection()
        
        [col,row] = [data.RasterXSize, data.RasterYSize]
        
        img = data.ReadAsArray()
        
        new_img = driver.Create(create_fname(path,target_folder),col,row,bands=4,eType = gdal.GDT_Float32)

        for k in range(1,5):
            # print(c,k)``
            l = k-1
            img[l][img[l]==0]=65535
            new_img.GetRasterBand(k).WriteArray(img[l])
            new_img.GetRasterBand(k).SetNoDataValue(65535)
        new_img.SetGeoTransform(geot)
        new_img.SetProjection(proj)
        data = None
        img = None
        q.task_done()
    print("change value done")

#################################   Execute   ####################
worker()


