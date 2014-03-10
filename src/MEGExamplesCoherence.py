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



    
cpath='/home/bejar/MEG/Data/'
#cres='/home/bejar/Documentos/Investigacion/MAG/res/'
cres='/home/bejar/Copy/MEG/Correlation/'
lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
        ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
        ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG'
        ,'control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
        ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
        ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']
lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]
#lnames=['comp10-MEG','comp10-MEG','comp10-MMN','comp12-MMN']
#lcol=[1,1,1,1]
#band='gamma-h'
#lband=['alpha','beta','gamma-l','gamma-h','theta','delta']
lband=['beta','gamma-l','gamma-h','theta','delta']
for band in lband:
    print band,
    examps=None
    for name in lnames:
        print name
        mats=scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
        data= mats['data']
        chann= mats['names']
    
        j=0
        mdata=None
        lsnames=[]
        for i in range(chann.shape[0]):
    #        cname=chann[i][0][0]
            cname=chann[i]
            if cname[0]=='A' and cname!='A53' and cname!='A31':# and cname!='A44' and cname!='A94':
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
                #if np.isnan(corr[i,j]) or corr[i,j]<0.7:
                examp[p]=cmatrix[i,j]
    #            if p in [1, 5367, 5353, 5668, 4971, 9634, 7867, 3366, 7278, 604, 6881, 2217, 8349, 9401, 5708, 9590, 7460, 4519, 664]:
    #                print lsnames[i],lsnames[j]
                p+=1
                
        if examps==None:
            examps=examp
        else:
            examps=np.vstack((examps,examp))
    
    print examps.shape




    X=examps
    Y=np.array(lcol)
    patdata={}
    patdata['data']=X
    patdata['classes']=Y
    scipy.io.savemat(cres+'patcoherence-'+band,patdata,do_compression=True)
    
