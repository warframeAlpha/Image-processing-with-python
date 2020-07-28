## This program calculate a band math and add the result with the original image.
import gdal
import os
import numpy as np
import queue, threading

q = queue.Queue()
def create_fname(path):
    slash = r'/'
    
    fname = ''
    for i in range(path.rfind(slash),len(path)):
        fname = fname + path[i]
    fname = 'result_folder'+fname
    return fname

def worker():
    while q.empty == False:
        path = q.get()
        data = gdal.Open(path)
        geot = data.GetGeoTransform()
        proj = data.GetProjection()
        [col,row] = [data.RasterXSize, data.RasterYSize]
        img = data.ReadAsArray()
        [R,NIR] = [img[0],img[1]]
        new_band = (NIR-R)/(NIR+R)
        driver = gdal.GetDriverByName('ENVI')
        new_img = driver.Create(create_fname(path),col,row,bands=5,eType = gdal.GDT_Float32)
        new_img.SetGeoTransform(geot)
        new_img.SetProjection(proj)
        for k in range(1,5):
            l = k-1
            img[l][img[l]==0]=65535
            new_img.GetRasterBand(k).WriteArray(img[l])
            new_img.GetRasterBand(k).SetNoDataValue(65535) 
        new_img.GetRasterBand(5).WriteArray(new_band)
        data = None
        img = None
        q.task_done()

# send thirty task requests to the worker
folder = 'E:/Deep_frustrating/masked_pansharpening_results' #The folder with masked pan sharpening results
flist = os.listdir(folder) 
for f in flist:
    if f.endswith('masked'):
        full_path = folder+'/'+f
        q.put(full_path)
print('All task requests sent\n', end='')
# turn-on the worker thread
for workers_num in range(5):
    threading.Thread(target=worker, daemon=True).start()
# block until all tasks are done
q.join()
print('All work completed')
