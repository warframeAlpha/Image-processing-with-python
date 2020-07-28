import gdal
import numpy
import os
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

def worker():
    driver = gdal.GetDriverByName('ENVI')
    folder = 'E:/Deep_frustrating/ENVI_tiles_1250'
    sub_folder = os.listdir(folder)
    print(sub_folder)
    for sub in sub_folder:
        q = queue.Queue()
        target_folder = 'E:/Deep_frustrating/ENVI_tiles_1250_65535/'+sub
        os.mkdir(target_folder)
        fpath = folder+'/'+sub
        files = os.listdir(fpath)
        for f in files:
            if f.endswith('subset'):
                full_path = fpath+'/'+f
                q.put(full_path)
        threading.Thread(target=change_value, args=(q,target_folder,f,driver), daemon=True).start()
        threading.Thread(target=change_value, args=(q,target_folder,f,driver), daemon=True).start()
        threading.Thread(target=change_value, args=(q,target_folder,f,driver), daemon=True).start()
        threading.Thread(target=change_value, args=(q,target_folder,f,driver), daemon=True).start()
        # change_value(q,target_folder,driver,f)
        q.join()
def change_value(q,target_folder,f,driver):
    while q.empty == False:
        path = q.get()
        data = gdal.Open(path)
        geot = data.GetGeoTransform()
        proj = data.GetProjection()
        [col,row] = [data.RasterXSize, data.RasterYSize]
        img = data.ReadAsArray()
        fname = target_folder+'/'+f
        new_img = driver.Create(fname,col,row,bands=5,eType = gdal.GDT_Float32)
        new_img.SetGeoTransform(geot)
        new_img.SetProjection(proj)
        for k in range(1,4):
            l = k-1
            img[l][img[l]==0]=65535
            new_img.GetRasterBand(k).WriteArray(img[l])
            new_img.GetRasterBand(k).SetNoDataValue(65535)
    data = None
    img = None
    q.task_done()

#################################   Execute   ####################
worker()