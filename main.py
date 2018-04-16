#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 13:45:41 2017

@author: Andrea Gerardo Russo Eng., PhD candidate
Department of Political, Social, and Communication Science
University of Salerno 
via Giovanni Paolo II, 132
84084 Fisciano (SA), Italy 
e-mail: andrusso@unisa.it

"""

import os
import numpy as np
from make_circle import make_circle
import time
from sklearn.externals import joblib

##############################################################################
from functions import load_file, v_mask ,mean_aparc, single_rad2cart 
from functions import single_surf_selection,single_cube_bin_pattern 
from functions import rad_sampling, euclidean_selection, tRAS


###############################################################################
def acps_main(subs_dir, subs):
#    clf = joblib.load('clf.pkl')
    clf = joblib.load('ACPS_clf.pkl')
    print('T1_Classifier loaded!')
    
    ##############################################################################
    
    os.system('clear')

    
    ##############################################################################
    
    for sub_directory in subs:
        start = time.time()
        print(os.path.basename(sub_directory))
        if subs_dir != '':
            sub_directory = os.path.join(subs_dir,sub_directory)        
        bmask,ribbon, aparc, wm_low = load_file(sub_directory) 
        print('Files loaded!')
        #masking volumes
        gm=v_mask(ribbon,bmask)
        pos_gm = gm[gm>0]
        min_gm = pos_gm.min()
        max_gm = pos_gm.max()
        slope1 = 110-max_gm
        slope2 = 110-min_gm 
        mean_regions = mean_aparc(aparc,bmask)
        print('Thresholds estimated!')
        sp4=np.empty((0,3))
        
        
        
        ###########################################################################
        for n_slice in range(0,255):
            print ('Slice '+ str(n_slice))
            ima = gm[:,:,n_slice]
            imax = np.mean(ima,axis=1)
            if np.sum(imax)>0:
                non_zero_coords = np.nonzero(ima)
                non_zero_idx = zip(non_zero_coords[0],non_zero_coords[1])
                center = make_circle(non_zero_idx)
                xc = center[0]
                yc = center[1]
                radmax = center[2]
                info = [ima,center,mean_regions,aparc, n_slice,slope1,slope2,wm_low]
                wmLow_cp = rad_sampling(ima,radmax,xc,yc,slope1,slope2,n_slice,wm_low)
                if wmLow_cp:
                    sp = [single_rad2cart(rad_cp,info) for rad_cp in wmLow_cp] 
                    sp = [x for x in sp if x != []]
                    if sp:
                        sp = list(np.unique(np.asarray(sp),axis=0))
                        indices = [single_surf_selection(cp,info) for cp in sp]
                        indices = np.asarray([0 if i==[] else i for i in indices])
                        if indices.any():
                            sp = np.asarray(sp)
                            sp2 = sp[indices==0,:]
                        else:
                            sp2 = np.empty((0,0))                       
                        if sp2.size!=0:
                           sp3 = euclidean_selection(ima,sp2,6)
                           if sp3.size!=0:
                              sp4 = np.append(sp4,sp3,axis=0)
        
        sp4 = np.delete(sp4,0,axis=0)
        
        
        sp5 = np.asarray([single_cube_bin_pattern(cp,bmask) for cp in list(sp4)])
        sp5 = np.delete(sp5,np.where(~sp5.any(axis=0))[0][0],axis=1)
        ###########################################################################
        
        features = sp5
        print('Features loaded!')
        preds = clf.predict(features)
        print('Predictions done!')
        
        control_points = sp4[preds==1,:]    
        tRAS(control_points,sub_directory)
        end = time.time() 
        print('Number of CPs placed: '+ str(control_points.shape[0]))       
        print('Time elapsed:'+ str(end-start))
        
        
        ##############################################################################
        print('DONE')   
        
    with open(subs_dir + 'CP_log.dat', "a") as myfile:
        myfile.write('Written by ACPS algorithm (DipMedChi, Lab University '+
                         'of Salerno (Italy))')