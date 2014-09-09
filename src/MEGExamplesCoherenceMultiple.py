# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:41:42 2013

Computes the scaled correlation matrix of the MEG signals
and generates a matlab file for each patient

Divides the signal in multiple files

@author: bejar
"""


import scipy.io
from numpy import mean, std
import matplotlib.pyplot as plt
from pylab import *
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
from nitime.algorithms.cohere import coherence_bavg
import nitime.timeseries as ts
from scipy import corrcoef

from sklearn.decomposition import PCA,KernelPCA


def coherenceMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    for length in range(linit,lend,lstep):
        a=ts.TimeSeries(mdata[:,length:length+lstep],sampling_rate=678.19)
        corrs=coherence_bavg(a)
        corr+=corrs    
    corr/=nstep
    return corr


    
cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/MEG/Resultados'
# lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
#         ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
#         ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG'
#         ,'control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
#         ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
#         ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']

lnames=[('control1-MMN',0),('control2-MMN',0),('control3-MMN',0),('control4-MMN',0)
       ,('control5-MMN',0),('control6-MMN',0),('control7-MMN',0)
       ,('comp1-MMN',1),('comp3-MMN',1),('comp4-MMN',1) ,('comp5-MMN',1)
       ,('comp6-MMN',1),('comp7-MMN',1),('comp13-MMN',1)
       ,('descomp1-MMN',2),('descomp3-MMN',2),('descomp4-MMN',2),('descomp5-MMN',2)
       ,('descomp6-MMN',2),('descomp7-MMN',2)]

badchannels=['A53','A31','A94']

ntimes = 10

examps = {}

for i in range(ntimes):
    examps[i] = None


lcol = []
band='all'
for name,cl in lnames:
    print name
    lcol.append(cl)
    mats=scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
    data= mats['data']
    chann= mats['names']
    natt=0
    mdata = None
    lsnames = []
    for i in range(chann.shape[0]):
        cname=chann[i]
        if cname[0]=='A' and not cname.strip() in badchannels:
            natt+=1
            lsnames.append(cname)
            if mdata == None:
                mdata=data[i]
            else:
                mdata=np.vstack((mdata,data[i]))
    
    #--            
    size = mdata.shape[1]
    blength=int(size/ntimes)        
    for time in range(ntimes):
        print time           
        cmatrix=coherenceMatrix(mdata,time*blength,(time+1)*blength,10)
        examp=np.zeros((natt*(natt-1)/2))
        print natt,mdata.shape,cmatrix.shape,examp.shape
        
        p=0
        for i in range(cmatrix.shape[0]-1):
            for j in range(i+1,cmatrix.shape[0]):
                examp[p]=cmatrix[i,j]
                p+=1
                
        if examps[time] == None:
            examps[time]=examp
        else:
            examps[time]=np.vstack((examps[time],examp))
    
        print examps[time].shape
    
    
for i in range(ntimes):    
    X=examps[i]
    Y=np.array(lcol)
    patdata={}
    patdata['data']=X
    patdata['classes']=Y
    scipy.io.savemat(cres+'patcoher-'+band+'-'+str(i),patdata,do_compression=True)

