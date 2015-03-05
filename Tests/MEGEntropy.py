# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:35:01 2013

@author: bejar
"""
import numpy as np
import scipy.io



# The C_i^m part of the approximate entropy
def Cmi(signal,i,m,r):
    count=0
    for n in range(len(signal)-m):
        dist=np.amax(signal[i:i+m-1]-signal[n:n+m-1])
        if dist<r*r:
            count+=1
    return count/(len(signal)-m)
    
# Computes the approximate entropy of a signal
def approximateEntropy(signal,m,thres):
    vres=0
    for i in range(len(signal)-m):
        cm=Cmi(signal,i,m,thres)
        cml=Cmi(signal,i,m+1,thres)
        print cm,cml,vres
        vres+=np.log(cm/cml)
    return vres/(len(signal)-m)
    
    
cpath='/home/bejar/MEG/Data/control/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
#name='MMN-201205251030'
name='control1-MMN'
mats=scipy.io.loadmat( cpath+name+'.mat')
data= mats['data']
chann=mats['names']


v=approximateEntropy(data[0:100,50],2,0.01)

print v