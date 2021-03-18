# rec_shrinking.py
import laspy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
start=time.time()
#import rectangles 14, 23
rec=pd.read_csv('rectangles.csv')
las=laspy.file.File('20200218_Icrisat1020.las')
result=dict()
result['x1']=[]
result['y1']=[]
result['x2']=[]
result['y2']=[]
result['x3']=[]
result['y3']=[]
result['x4']=[]
result['y4']=[]
'''
# show relationship
plt.scatter(rec['x1'][0],rec['y1'][0],label='1')
plt.scatter(rec['x2'][0],rec['y2'][0],label='2')
plt.scatter(rec['x3'][0],rec['y3'][0],label='3')
plt.scatter(rec['x4'][0],rec['y4'][0],label='4')
plt.legend()
plt.show()
'''
# rec['x1']
for i in range(5):
    flag=True
    x1=rec['x1'][i]
    y1=rec['y1'][i]
    x2=rec['x2'][i]
    y2=rec['y2'][i]
    x3=rec['x3'][i]
    y3=rec['y3'][i]
    x4=rec['x4'][i]
    y4=rec['y4'][i]

    #y=mx+k, we need the line functions between points 1 2 3 4 (see relationship)
    m12=(y2-y1)/(x2-x1) 
    m34=(y3-y4)/(x3-x4) 
    m14=(y4-y1)/(x4-x1) 
    m23=(y3-y2)/(x3-x2)
    k12=y1-m12*x1
    k34=y4-m34*x4
    k14=y1-m14*x1
    k23=y2-m23*x2
    # print(m12,m34,m14,m23,k12,k34,k14,k23)
    # define the window
    index14=las.y>m14*las.x+k14
    index23=las.y<m23*las.x+k23
    index_long=np.logical_and(index14,index23)
    old_height=87878787
    n=0
    step=0.08
    while flag == True:
        #left line:y=m(x-step*n)+k, 
        indexl=las.y<m34*(las.x-step*n)+k34
        indexr=las.y>m34*(las.x-step*(n+1))+k34
        index_short=np.logical_and(indexl,indexr)
        indexx=np.logical_and(index_short,index_long)
        new_height=np.mean(las.z[indexx])
        if new_height-old_height<1:
            old_height=new_height
            n=n+1
        else:
            rec_x3=x3+step*n
            rec_y3=m23*rec_x3+k23
            rec_x4=x4+step*n
            rec_y4=m14*rec_x4+k14
            result['x4'].append(rec_x4)
            result['y4'].append(rec_y4)
            result['x3'].append(rec_x3)
            result['y3'].append(rec_y3)
            flag=False
    n=0
    old_height=87878787

    while flag == False:
        #right line:y=m(x+step*n)+k, 
        indexl=las.y<m12*(las.x+step*(n+1))+k12
        indexr=las.y>m12*(las.x+step*n)+k12
        index_short=np.logical_and(indexl,indexr)
        indexx=np.logical_and(index_short,index_long)
        new_height=np.mean(las.z[indexx])
        if new_height-old_height<1:
            old_height=new_height
            n=n+1
        else:
            rec_x1=x1+step*n
            rec_y1=m14*rec_x1+k14
            rec_x2=x2+step*n
            rec_y2=m23*rec_x2+k23
            result['x2'].append(rec_x2)
            result['y2'].append(rec_y2)
            result['x1'].append(rec_x1)
            result['y1'].append(rec_y1)
            flag=True


rec=pd.DataFrame(result)
rec.to_csv('threshold1.csv')
end=time.time()
print('time',end-start)
