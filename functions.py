#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:02:30 2017

@author: Andrea Gerardo Russo Eng., PhD candidate
Department of Political, Social, and Communication Science
University of Salerno 
via Giovanni Paolo II, 132
84084 Fisciano (SA), Italy 
e-mail: andrusso@unisa.it

"""
from nibabel.freesurfer.mghformat import load
import numpy as np 
import pandas as pd
import math
import copy
from sklearn.metrics.pairwise import pairwise_distances
import time




###############################################################################
##                            LOAD FILE                                      ##
###############################################################################
def load_file(directory):
    brainmask = load(directory + '/mri/brainmask.mgz');
    ribbon = load(directory + '/mri/ribbon.mgz')
    aparc = load(directory+'/mri/aparc+aseg.mgz')
    
    segment = []
    with open(directory + '/mri/segment.dat', "r") as f:
        segment.append(f.readlines())
            
    content=segment[0] 
    string_3 = content[2]
    wm_low = float(string_3[40:-1])
       
    bmask_data = brainmask.get_data()
    ribbon_data = ribbon.get_data()
    aparc_data = aparc.get_data()
    return bmask_data,ribbon_data,aparc_data, wm_low;





###############################################################################   
##                            MASK                                           ##
###############################################################################
def v_mask(ribbon,bmask):
    gm = bmask*((ribbon==42) | (ribbon==3))
    return gm

###############################################################################   
##                            MEAN APARC                                     ##
###############################################################################
def mean_aparc(aparc,bmask):    
    atlas = pd.read_csv('atlas.csv')
    ids = atlas['#No.']
    mean_regions = pd.DataFrame([],index=ids)
    print ('Thresholds estimation....')
    for i,j in zip(ids, range(0,atlas.shape[0])):
        tmp = copy.deepcopy(bmask)
        tmp[aparc!=i] = 0
        mean_regions.at[i,'tGMs'] = np.mean(tmp[tmp>0].flatten()) + 2*(np.std(tmp[tmp>0].flatten()))

    return mean_regions

###############################################################################   
##                            MASK                                           ##
###############################################################################        

def rad_sampling(ima,radmax,xc,yc,slope1,slope2,n_slice,wm_low):
    radvec = np.linspace(0,1,360)
    thetavec = np.linspace(0,2*math.pi,360)  
    P = np.zeros((radvec.shape[0],thetavec.shape[0]))
    dP = np.zeros((radvec.shape[0],thetavec.shape[0]))
    wmLow_cp = []
      
    for j,theta in enumerate(thetavec):
        for i,r in enumerate(radvec):
            xp = int(np.ceil(xc + r*radmax*math.cos(theta)))
            yp = int(np.ceil(yc + r*radmax*math.sin(theta)))
            P[i,j] = ima[xp,yp]
            

        dP[:,j] = np.append(np.diff(P[:,j]),0)
        
        if (sum(P[:,j]))!=0:
            iCp = np.argsort(dP[:,j])
            for idx in iCp:
                if dP[idx,j]!=0:
                    if (dP[idx,j]>slope1 and dP[idx,j]<slope2):
                        if P[idx,j]>wm_low and P[idx,j]<110:
                            wmLow_cp.append([radvec[idx],theta,P[idx,j]])
    return wmLow_cp


###############################################################################   
##                            SINGLE RAD2CART                                ##
###############################################################################





def single_rad2cart(rad_cp,info):
    xc = info[1][0]
    yc = info[1][1]
    radmax = info[1][2]
    mean_regions = info[2]
    aparc = info[3]
    n_slice = info[4]
    
    aparc_slice = aparc[:,:,n_slice]
    result = []
    xp = int(np.ceil(xc + rad_cp[0]*radmax*math.cos(rad_cp[1])))
    yp = int(np.ceil(yc + rad_cp[0]*radmax*math.sin(rad_cp[1])))
    if mean_regions.index.contains(aparc_slice[xp,yp]):
        reg_tGM = mean_regions.loc[aparc_slice[xp,yp]].values[0]
        if (rad_cp[2]>reg_tGM and rad_cp[2]<110):
            result = [xp, yp, n_slice]
    return result



###############################################################################   
##                            SINGLE SURF SELECTION                          ##
###############################################################################

def single_surf_selection(cp,info):
    ima = info[0]
    index = []
    x=cp[0]
    y=cp[1]
    square = ima[x-1:x+2,y-1:y+2]
    if np.count_nonzero(square.flatten())!=9:
       index = 1
    return index  



###############################################################################   
##                           SINGLE CUBE PATTERN                             ##
###############################################################################

def single_cube_bin_pattern(cp,bmask):
    binary_pattern = np.zeros((6859))
    x = int(round(cp[0]))
    y = int(round(cp[1]))
    s = int(round(cp[2]))
    cp_intensity = bmask[x,y,s]
    cube = bmask[x-9:x+10, y-9:y+10,s-9:s+10]
    std_cube = np.std(cube.flatten())    
    binary_pattern = np.transpose((cp_intensity-cube.flatten())/std_cube) 
    return binary_pattern



###############################################################################   
##                            EUCLIDEAN SELECTION                            ##
###############################################################################

def euclidean_selection(ima,sp,thr):
   cp = copy.deepcopy(sp)
   index=[]
   if cp.shape[0]>1:
       mat_dist = pairwise_distances (cp, cp, metric='euclidean')
       if mat_dist.shape[0]>1:
           dist = np.tril(mat_dist*(np.triu(mat_dist)<thr))      
           idx = np.where((dist>0) & (dist<thr))
           if idx:
               indices = zip(idx[0],idx[1])
               for pair in indices:
                   coord1 = sp[pair[0],:]
                   coord2 = sp[pair[1],:]
                   int1 = ima[coord1[0],coord1[1]]
                   int2 = ima[coord2[0],coord2[1]]
                   if int1<int2:
                       index = np.append(index,pair[0])
                   else:
                       index = np.append(index,pair[1])
   cp = np.delete(cp,index,axis=0)

   return cp




###############################################################################   
##                            tRAS                                           ##
###############################################################################

def tRAS(cart_coordinates,sub):
    r = 128-(cart_coordinates[:,0])
    s = 128-(cart_coordinates[:,1])
    a = (cart_coordinates[:,2])-128     
    ras = np.array([r, a, s])
    ras = np.transpose(ras)
    points = ras[ras[:,0].argsort()]
    numpoints = np.size(points,axis=0)
    time_string = time.ctime()
    np.savetxt(sub + '/tmp/control.dat', points, delimiter=' ')
    with open(sub + '/tmp/control.dat', "a") as myfile:
        myfile.write('numpoints ' + str(numpoints) + '\n')
        myfile.write('useRealRAS 0 ' + '\n')
        myfile.write('written by ACPS algorithm (DipMedChi Lab, University '+
                     'of Salerno (Italy)) on ' + time_string)

       
###############################################################################  
   
   
    