# This scipt aims to help select the appropriate training data for deep learning. Our goal is to detect the building. 
#Thus, training data should contain an number of buildings. The image we use is pleades image, which cannot derive NDBI.
# As a result, I will use NDVI instead. 
# Computing the percentile of NDVI and choosing the threshold (by an MS student) so that we can remove those image that contain mostly vegetation.
import gdal
import numpy as np
import os
import time
import _thread
import threading, queue
start = time.time()
def thread_task(q,img_size,step,thread_num):
    while q.empty()==False:
        subset_index=0
        img_name = q.get()
        target_folder='E:/Deep_frustrating/training_data/'+img_name
        img_path= 'E:/Deep_frustrating/masked_pahshapening_results_65535/'+img_name
        img = gdal.Open(img_path)
        [col,row] = [img.RasterXSize, img.RasterYSize]
#     step = 2500
        for i in range(0,row,step):
            starty = i
            endy = starty + step
            if endy>row:
                endy = row
                starty = endy-step
            for j in range(0,col,step):
                startx = j
                endx = startx+ step
                if endx >col:
                    endx = col
                    startx = endx-step
                img_array = img.ReadAsArray(startx,starty,step,step)
                
                if np.min(img_array) <65535:
                    #########From now, we start to compute NDVI and use it to decide whether to keep the image
                    #NDVI = (NIR-RED)/(NIR+RED) #NIR=3(band4) R=2(band3)
                    NDVI= (img_array[3]-img_array[2])/(img_array[3]+img_array[2])
                    ## If the image has no-data > 40% of all pixels-> discard
                    nan_index = img_array[3]==65535
                    nan_percentage = np.sum(nan_index)/(np.square(img_size))
                    if np.percentile(NDVI,20)<0.3 and nan_percentage<0.4: #20 and 0.3 are decided by an MS student, the value should be adjusted for other region.
                        subset_index += 1
                        output = target_folder+'/'+img_name+'_'+str(subset_index)+'subset'
                        command = str('gdal_translate  --config GDAL_CACHEMAX 16384 -of ENVI -srcwin '+str(startx)+' '+str(starty)+' '+str(img_size)+' '+str(img_size)+' '+img_path+' '+output)
                        os.system(command) 
        img = None
        q.task_done()

    
driver = gdal.GetDriverByName('ENVI')
path = 'E:/Deep_frustrating/masked_pahshapening_results_65535'
imgs = os.listdir(path)
q = queue.Queue()
for i in imgs:
    if i.endswith('masked'):
        q.put(i)
imgs=None

for thread_num in range(6):
    _thread.start_new_thread(thread_task,(q,2500,2500,thread_num))
q.join()
# while q.empty()==False:
#     print(q.get())
end = time.time()
t = end - start
print(t,'s')

