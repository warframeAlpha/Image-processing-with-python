import gdal
import numpy as np
import os
path = 'H:/Ender/banding/targets'
flist=['target1','target2','target3','target4']
fpath='H:/Ender/banding/20210512/nhs199_gryfn_1546/spectralview_or'
output_path='H:/Ender/banding/20210512/targets/nhs199_gryfn_1546'
flist2=[]
for i in os.listdir(fpath):
    if i.endswith('hdr'):
        continue
    if i.startswith('raw'):
        flist2.append(i)
# print(flist2)
for i in flist:
    input_target=path+'/'+i
    target=gdal.Open(path+'/'+i)
    # print(target.RasterXSize,target.RasterYSize)
    geoinfo = target.GetGeoTransform()
    # print(geoinfo)
    xOrigin = geoinfo[0]
    yOrigin = geoinfo[3]
    pixelWidth = geoinfo[1]
    pixelHeight = geoinfo[5]
    target=target.ReadAsArray()
    tr=np.argwhere(target ==1)
    ul_pixel=tr[0]
    lr_pixel=tr[-1]
    ulx=xOrigin+pixelWidth*ul_pixel[1] # ulx=x0+x_width*x
    uly=yOrigin+pixelHeight*ul_pixel[0] #uly=y0+y_height*x (y_height is negtive)
    lrx=xOrigin+pixelWidth*lr_pixel[1]
    lry=yOrigin+pixelHeight*lr_pixel[0]
    print(ul_pixel)
    
    for j in flist2:
        input_file=fpath+'/'+j
        output_file=output_path+'/'+j+'_'+i
        command = str('gdal_translate  --config GDAL_CACHEMAX 16384 -of ENVI -projwin '+str(ulx)+' '+str(uly)+' '+str(lrx)+' '+str(lry)+' '+input_file+' '+output_file)
        os.system(command)
    
    break