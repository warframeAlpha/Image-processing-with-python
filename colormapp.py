import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
'''
In this scrip, I assume that minimum temperature in the ocean is -10 and max is 50. The acceptable temperature for coral is 20~30.
colors = [
    (1, 0, 0), # not a good temp for coral
    (255, 153, 204), #close to the acceptable temp but still not acceptable
    (39, 246, 0), #20
    (0, 160, 0), #30
    (255, 153, 204), #close to the acceptable temp but still not acceptable
    (1, 0, 0), # not a good temp for coral
]
x = 31, y = 85 is the target coral reef island.
'''
flist = os.listdir('E:/Introduction_of_lab/OC')
for i in flist:
    if i.endswith('.tiff'):
        img = gdal.Open('E:/Introduction_of_lab/oc/'+i)
        col = img.RasterXSize
        row = img.RasterYSize
        img = img.ReadAsArray()
        img[img==-32767.0] = np.nan
        img.flags.writeable = False
        index = np.logical_and(30>=img,img>=20) # for the temp between 20 and 30
        
        ### Red color array
        red = img.copy()
        red[img<20.0] = 1+(img[img<20]+10)*254/30
        red[index] = 39-(img[index]-20)*39/10
        red[img>30] = 255-(img[img>30]-30)*254/30

        ### Green color array
        green = img.copy()
        green[img<20.0] = 0+(img[img<20]+10)*153/30
        green[index] = 246-(img[index]-20)*86/10
        green[img>30] = 153-(img[img>30]-30)*153/30

        ### Blue color array
        blue = img.copy()
        blue[img<20.0] = 0+(img[img<20]+10)*204/30
        blue[index] = 0
        blue[img>30] = 204-(img[img>30]-30)*254/30


        ### use matplotlib
        [red, green, blue] = [red/255,green/255,blue/255] #matplotlib read color from 0 to 1
        RGB = np.stack([red,green,blue],axis=2)
        print(RGB.shape)
        plt.imshow(RGB)
        plt.plot(13,85,marker = 'X',color = 'w')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.savefig('E:/Introduction_of_lab/SST_timeseries/'+i.replace('.tiff','.png'),transparent=True)