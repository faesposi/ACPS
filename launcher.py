#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 10:44:43 2018

@author: Andrea Gerardo Russo Eng., PhD candidate
Department of Political, Social, and Communication Science
University of Salerno 
via Giovanni Paolo II, 132
84084 Fisciano (SA), Italy 
e-mail: andrusso@unisa.it

"""
import glob
import os
from main import acps_main

with open("init.txt") as f:
    options = f.readlines()
options = [x.strip() for x in options] 

subs = []

#log = options[3]
subs_dir = options[3]
subs_1st = options[6]
if subs_1st is '*':
    subs = sorted(glob.glob(os.path.join(subs_dir,'*')))
    acps_main(subs_dir,subs)
else:
    subs = options[6:]
    acps_main(subs_dir,subs)
    
