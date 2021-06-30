import gdal
import os
import numpy as np
'''
This program converts tiff to jpeg. I assume that there will be only one dimension exceeds 65535, which is the max pixel number in a dimension for JPEG.
If not, change the code, subset images into 4 pieces.
'''

folder_path='H:/Ender/tempp' # Change this line. Don't use \, use /
flist=[] # the list for tiff files, f for files
for i in (os.listdir(folder_path)):
    if i.endswith('tiff') or i.endswith('tif'):
        flist.append(i)
for i in range(len(flist)): # if we need to do concurrent processing, we will need the len of flist
    # print('working on ',flist[i])
    input=folder_path+'/'+flist[i]
    if flist[i].endswith('tif'):
        output=folder_path+'/'+flist[i].replace('.tif','jpg')
    elif flist[i].endswith('tiff'):
        output=folder_path+'/'+flist[i].replace('.tiff','jpg')

    img=gdal.Open(input)
    if img.RasterXSize<65535 and img.RasterYSize<65535: # case1
        xsize=img.RasterXSize
        ysize=img.RasterYSize
        command=str('gdal_translate  --config GDAL_CACHEMAX 65536 -of JPEG -srcwin 0 0 '+str(xsize)+' '+str(ysize) +' '+input+' '+output)
        os.system(command)
    elif img.RasterXSize>65535 and img.RasterYSize<65535: # case2
        xsize=int(img.RasterXSize/2)
        xsize2=img.RasterXSize-xsize
        ysize=img.RasterYSize
        command=str('gdal_translate  --config GDAL_CACHEMAX 65536 -of JPEG -srcwin 0 0 '+str(xsize)+' '+str(ysize) +' '+input+' '+output)
        os.system(command)
        command2=str('gdal_translate  --config GDAL_CACHEMAX 65536 -of JPEG -srcwin '+str(xsize+1)+' 0 '+str(xsize2)+' '+str(ysize) +' '+input+' '+output)
        os.system(command2)
    elif img.RasterXSize<65535 and img.RasterYSize>65535: # case3
        xsize=img.RasterXSize
        ysize=int(img.RasterXSize/2)
        ysize2=img.RasterYSize-ysize
        command=str('gdal_translate  --config GDAL_CACHEMAX 65536 -of JPEG -srcwin 0 0 '+str(xsize)+' '+str(ysize) +' '+input+' '+output)
        command2=str('gdal_translate  --config GDAL_CACHEMAX 65536 -of JPEG -srcwin  0 '+' '+str(ysize+1)+str(xsize)+' '+str(ysize2) +' '+input+' '+output)
        os.system(command)
        os.system(command2)
