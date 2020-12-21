
# This program uses gdal_translate to subset muiltiple images. 
# For each image, this program generate several tiles with overlap areas.
import gdal
import os
import numpy as np
import time
# Use gdal_trnaslate to subset multiple images.
# Since our images contain large no-data area, I need to read the image as array to check whether the image is a empty image or not.
# The function only write image to the disk when the images are not empty
def subset_single(step,img_size):
    start = time.time()
    input_name = 'E:/Deep_frustrating/masked_pahshapening_results_65535/20170217_Pleiades_Taipei_ms_97_sharpening_masked'
    output_folder ='D:/TP_subset'
    [xsize,ysize] = [img_size,img_size]
    subset_index = 0
    img = gdal.Open(input_name)
    [col,row] = [img.RasterXSize,img.RasterYSize]
    for i in range(0,row,step):
        starty = i
        endy = starty + ysize
        if endy>row:
            endy = row
            starty = endy-ysize
        for j in range(0,col,step):
            startx = j
            endx = startx+ xsize
            if endx >col:
                endx = col
                startx = endx-xsize
            img_array = img.ReadAsArray(startx,starty,xsize,ysize)
            if np.min(img_array) < 65535:
                subset_index += 1
                output = output_folder+'/20170217_Pleiades_Taipei_ms_97_sharpening_masked_'+str(subset_index)+'subset'
                command = str('gdal_translate  --config GDAL_CACHEMAX 16384 -of ENVI -srcwin '+str(startx)+' '+str(starty)+' '+str(xsize)+' '+str(ysize)+' '+input_name+' '+output)
                os.system(command) 
    img = None
    end = time.time()
    t = start - end
    print(t,'second')
def translate_multiple(path,step,img_size):
    start = time.time()
    while "\\" in path is True:
        path = path.replace("\\","/")
    img_list = os.listdir(path)
#     step = 1250
    [xsize,ysize] = [img_size,img_size]
    for file in img_list:
        subset_index = 0
        if file.endswith('masked'):
            sub_path= 'E:/Deep_frustrating/tiles_2400_65535/'+str(file)+'_subset'
            os.mkdir(sub_path)
#         print(files)
            fname = path+'/'+file
            print(fname)
            img = gdal.Open(fname)
            [col,row] = [img.RasterXSize,img.RasterYSize]
            for i in range(0,row,step):
                starty = i
                endy = starty + ysize
                if endy>row:
                    endy = row
                    starty = endy-ysize
                for j in range(0,col,step):
                    startx = j
                    endx = startx+ xsize
                    if endx >col:
                        endx = col
                        startx = endx-xsize
                    img_array = img.ReadAsArray(startx,starty,xsize,ysize)

                    if np.min(img_array) <65535:
                        subset_index += 1
                        output = sub_path+'/'+file+'_'+str(subset_index)+'subset'
                        command = str('gdal_translate  --config GDAL_CACHEMAX 16384 -of ENVI -srcwin '+str(startx)+' '+str(starty)+' '+str(xsize)+' '+str(ysize)+' '+fname+' '+output)
                        os.system(command) 
            img = None
    end = time.time()
    t = start - end
    print('gdal_translate multi files took ',t,' seconds')
def warp_multiple(path):
    output_folder = 'E:/Deep_frustrating/masked_pahshapening_results_65535/'
    # this can change no-data value
    start = time.time()
    while os.sep in path is True:
        path = path.replace(os.sep,"/")
    flist = os.listdir(path)
    for f in flist:
        if f.endswith('masked'):
            fname = path +'/'+f
            output = output_folder+f
            command = str('gdalwarp -wo NUM_THREADS=6 -ot UINT16 -srcnodata 0 -dstnodata 65535 -wm 17179860387 -of ENVI '+fname+' '+output)
            os.system(command) 
    end = time.time()
    t = start - end
    print('warp took ',t, 'seconds')

path= 'E:/Deep_frustrating/masked_pahshapening_results_65535'
translate_multiple(path,step=2400,img_size = 2500)  
# subset_single(1250,2500)
