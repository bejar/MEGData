# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:41:42 2013

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


def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    liter= [linit+(i*lstep) for i in range(nstep)]
    for length in liter:
        a=ts.TimeSeries(mdata[:,length:length+lstep],sampling_rate=678.19)
        corrs=coherence_bavg(a)
        corr+=corrs    
    corr/=nstep
    return corr



    
cpath='/home/bejar/MEG/DataTest/'
#cres='/home/bejar/Documentos/Investigacion/MAG/res/'
cres='/home/bejar/Copy/MEG/Correlation/'
# lnames=[('control1-MMN',0),('control2-MMN',0),('control3-MMN',0),('control4-MMN',0)
#        ,('control5-MMN',0),('control6-MMN',0),('control7-MMN',0)
#        ,('comp1-MMN',1),('comp3-MMN',1),('comp4-MMN',1) ,('comp5-MMN',1)
#        ,('comp6-MMN',1),('comp7-MMN',1),('comp13-MMN',1)
#        ,('descomp1-MMN',2),('descomp3-MMN',2),('descomp4-MMN',2),('descomp5-MMN',2)
#        ,('descomp6-MMN',2),('descomp7-MMN',2)]


lnames=[('control8-MMN',0),('control9-MMN',0),('control10-MMN',0)
       ,('comp2-MMN',1),('comp8-MMN',1),('comp9-MMN',1)
       ,('descomp10-MMN',2),('comp12-MMN',2)]

lband=['all','gamma-l','gamma-h']
badchannels=['A53','A31','A94']

for band in lband:
    print band,
    examps=None
    lcol = []
    for name,cl in lnames:
        lcol.append(cl)
        print name
        mats=scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
        data= mats['data']
        chann= mats['names']
    
        j=0
        mdata=None
        lsnames=[]
        for i in range(chann.shape[0]):
    #        cname=chann[i][0][0]
            cname = chann[i][0][0]
            if cname[0]=='A' and not cname.strip() in badchannels:
                j+=1
                lsnames.append(cname)
                if mdata==None:
                    mdata=data[i]
                else:
                    mdata=np.vstack((mdata,data[i]))
            else:
                print cname,i
    #    print lsnames
        cmatrix=correlationMatrix(mdata,0,mdata.shape[1],10)
        print j,mdata.shape
        examp=np.zeros((j*(j-1)/2))
        
        p=0
        for i in range(cmatrix.shape[0]-1):
            for j in range(i+1,cmatrix.shape[0]):
                examp[p]=cmatrix[i,j]
                p+=1
                
        if examps==None:
            examps=examp
        else:
            examps=np.vstack((examps,examp))
    
    print examps.shape




    X = examps
    Y = np.array(lcol)
    patdata={}
    patdata['data']=X
    patdata['classes']=Y
    scipy.io.savemat(cres+'patcoherence-test-'+band,patdata,do_compression=True)
    
