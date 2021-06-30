'''
This code is the python version of Behrokh's matlab code.
The python version is accelerated by massively applying numpy function to reduce the usage of for loop. Do not add them back.
Most variables' name are not changed
'''
import laspy
import numpy as np
import os
from scipy.stats import skew as skewness
from scipy.spatial import ConvexHull 
from scipy.spatial import cKDTree as KDTree

############################### Import data ########################################
temp1=[] 
n=4800# Ask: what is n
line=1 # line count
path='H:/Ender/LAI/From_Behrokh/data'# file path
flist=os.listdir(path)
S=[]
for i in flist:
    if i.endswith('.las'):
        S.append(path+'/'+i)
        las=laspy.file.File(path+'/'+i) #Ask: only read one las or read several las?
        break
x=np.array(las.x)
y=np.array(las.y)
z=np.array(las.z)
All=np.vstack((x,y,z))
VCI_bin_const=0
Plane_Q3=[]
Plane_Q1=[]
# print(S)
############################### Height Indices ########################################
max_z=np.quantile(z,0.95)
min_z=0.1
QQ_all=[]

indexx=np.logical_and(z>=min_z, z<=max_z)
p=np.sum(indexx) # num of points within max z and min z
Z_over10=z[indexx] # points with height higher than 10 cm
All_over10=np.array([x[indexx],y[indexx],z[indexx]]) 

lessthanmin=z<0.1
qqq=np.sum(lessthanmin) #num of points whose z<0.1m
# LPI=-np.log(qqq/len(z)) # laser penetration index
LPI=qqq/len(z) # Behrokh's new version
Q3=np.quantile(Z_over10,0.75) # 75% height
Q1=np.quantile(Z_over10,0.60) # 60% height
# Ask: What's the structure of temp1
temp1.append([n])
temp1.append([LPI])
temp1.append([np.mean(Z_over10)])
temp1.append([skewness(Z_over10)])
temp1.append([np.std(Z_over10)])
temp1.append([np.quantile(Z_over10,0.75)])

############################### Vertical complex index ########################################
HB_const=4 # number of sections that we cut the trees into (in z direction)
Q_all=[]
bin=(max_z-min_z)/HB_const # the height of each section
VCI_HB_const_temp=[]

for i in range(HB_const):
    indexx=None
    q=None
    min_bin=min_z+bin*i
    max_bin=min_z+bin*(i+1)
    indexx=np.logical_and(Z_over10>=min_bin,Z_over10<max_bin)
    q=np.sum(indexx)# number of points in a bin
    Q_all.append([q]) 
    VCI_HB_const_temp.append(q/p*np.log(q/p)) # p=num of points within max z and min z

VCI_HB_const=-np.sum(VCI_HB_const_temp)/np.log(HB_const)
temp1.append([VCI_bin_const])
# CAP
############################### Extracting points of Q1 and  planes ########################################
acceptable_points=10
radius_cluster=0.15
indexx_Q3=np.logical_and(z<(Q3+0.05), z>(Q3-0.05))
Plane_Q3=np.array([x[indexx_Q3],y[indexx_Q3],z[indexx_Q3]])
indexx=None

indexx_Q1=np.logical_and(z<(Q1+0.05), z>(Q1-0.05))
Plane_Q1=np.array([x[indexx_Q1],y[indexx_Q1],z[indexx_Q1]])
############################### Area of Q3 in a plot CAP ########################################

def cluster_MV(input,radius,acceptable_points):
    # set method
    #https://stackoverflow.com/questions/4842613/merge-lists-that-share-common-elements
    All= input
    rS=radius
    pairs=[(All[0][i],All[1][i],All[2][i]) for i in range(All.shape[1])]
    Mdl=KDTree(pairs)
# Now I will loop through every point to cluster them. 
    cluster=[[] for i in range(len(pairs))]
    for i in range(len(pairs)):
        idx_S=Mdl.query_ball_point(pairs[i],rS)
        # print(idx_S)
        # print(type(idx_S)) #list
        for j in idx_S:
            cluster[i].append(pairs[j])
        # print(pairs[i])
        # print(cluster[i])
    # Merge clusters if they have a common point using set
    out = []
    while len(cluster)>0:
        first, *rest = cluster
        first=set(first)
        lf = -1
        while len(first)>lf: # this condition means there is no intersection between first and rest
            lf = len(first)

            rest2 = []
            for r in rest:
                if len(first.intersection(set(r)))>0:
                    first |= set(r)
                else:
                    rest2.append(r)     
            rest = rest2

        out.append(first)
        cluster = rest
        point_number=[]
    for i in range(len(out)):
        point_number.append(len(out[i]))
    point_number=np.array(point_number)
    out2=[]
    for i in range(len(out)):
        if point_number[i]>acceptable_points:
            out2.append(out[i])
    out2=list(out2)
    for i in range(len(out2)):
        out2[i]=list(out2[i])

    return out2

 
    #time1=toc # Ask: what is this, this does not return to main
    #save sim_time time1 Ask: what is this, this does not return to main

clust=cluster_MV(Plane_Q3,0.15,10)
# Calculate area
# https://stackoverflow.com/questions/19873596/convex-hull-area-in-python#:~:text=Convex%20hull%20is%20simply%20a,find%20area%20of%202D%20polygon.&text=in%20which%20pts%20is%20array,%2C%20a%20(nx2)%20array.&text=You%20could%20just%20use%20the,spatial%20.
area=0
for i in clust:
    area=area+ConvexHull(i).area
temp1.append([area]) # CAP=sum of area

# Volumne of a row
######## the boundary shrinks towards the interior of the hull to envelop the points ###########
acceptable_points1=15 
radius_cluster1=0.08 #1 series uses Q1
Final_points1=np.array(All_over10)
clust1=cluster_MV(Final_points1,radius_cluster1,acceptable_points1)
vol=0
for i in clust1:
    vol=vol+ConvexHull(i).volume
temp1.append(vol)

print(temp1)
# matlab line215
# outfile1=pathname
n=0
z=list(z)
print(type(z))
QQ=Q3-0.05
QQQ=Q3+0.05
for i in range(len(z)):

    if z[i]>(QQ) and z[i]<(QQQ):
        n=n+1
print(n)

print('-----------------------')
print('length of Plane_Q3=',len(Plane_Q3))
