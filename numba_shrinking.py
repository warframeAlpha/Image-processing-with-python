from numba import njit, types, vectorize
import numpy as np
import laspy
import time
import pandas as pd
import random

start=time.time()
#import rectangles 14, 23
rec=pd.read_csv('rectangles.csv')
# las=laspy.file.File('20200218_Icrisat1020.las')
las=laspy.file.File('DSM.las')
nn=np.full(50,-1)
mm=np.full(50,-1)
result=dict()
result['x1']=np.full(50,-1)
result['y1']=np.full(50,-1)
result['x2']=np.full(50,-1)
result['y2']=np.full(50,-1)
result['x3']=np.full(50,-1)
result['y3']=np.full(50,-1)
result['x4']=np.full(50,-1)
result['y4']=np.full(50,-1)

@njit()
def shrink(i,step,threshold):
    old_height=878787
    flag=True
    n=0
    while flag == True:
        print(n)
                #left line:y=m(x-step*n)+k, 
        indexl=las.y<m34*(las.x-step*n)+k34
        indexr=las.y>m34*(las.x-step*(n+1))+k34
        index_short=np.logical_and(indexl,indexr)
        indexx=np.logical_and(index_short,index_long)
        try:
            new_height=np.median(las.z[indexx])
            if new_height-old_height<threshold:
                old_height=new_height
                n=n+1
                print(n)
            else:
                rec_x3=x3+step*n
                rec_y3=m23*rec_x3+k23
                rec_x4=x4+step*n
                rec_y4=m14*rec_x4+k14
                result['x4'][i]=rec_x4
                result['y4'][i]=rec_y4
                result['x3'][i]=rec_x3
                result['y3'][i]=rec_y3
                nn[i]=n
                flag=False
        except:
            n=n+1
            print(n)
    n=0
    old_height=87878787
    while flag == False:
        #right line:y=m(x+step*n)+k, 
        indexl=las.y<m12*(las.x+step*(n+1))+k12
        indexr=las.y>m12*(las.x+step*n)+k12
        index_short=np.logical_and(indexl,indexr)
        indexx=np.logical_and(index_short,index_long)
        try:
            new_height=np.median(las.z[indexx])
            if new_height-old_height<threshold:
                old_height=new_height
                n=n+1
                print(n)
            else:
                rec_x1=x1+step*n
                rec_y1=m14*rec_x1+k14
                rec_x2=x2+step*n
                rec_y2=m23*rec_x2+k23
                result['x2'][i]=rec_x2
                result['y2'][i]=rec_y2
                result['x1'][i]=rec_x1
                result['y1'][i]=rec_y1
                mm[i]=n
                flag=True
        except:
            n=n+1
            print(n)
for i in range(50):
    shrink(i,0.08,0.5)
