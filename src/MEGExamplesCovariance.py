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

from scipy import corrcoef,cov

from sklearn.decomposition import PCA,KernelPCA


def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    liter= [linit+(i*lstep) for i in range(nstep)]
    print liter, len(liter),lend
    zz = 0
    for length in liter:
        corrs = cov(mdata[:,length:length+lstep])
        corr += corrs
        zz += 1
        print length, length+lstep,
    print zz
    corr /= nstep
    return corr


    
cpath='/home/bejar/MEG/Data/'
#cres='/home/bejar/Documentos/Investigacion/MAG/res/'
cres='/home/bejar/Copy/MEG/Correlation/'
# lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
#         ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
#         ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG'
#         ,'control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
#         ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
#         ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']
# lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]

lnames=[('control1-MMN',0),('control2-MMN',0),('control3-MMN',0),('control4-MMN',0)
       ,('control5-MMN',0),('control6-MMN',0),('control7-MMN',0)
       ,('comp1-MMN',1),('comp3-MMN',1),('comp4-MMN',1) ,('comp5-MMN',1)
       ,('comp6-MMN',1),('comp7-MMN',1),('comp13-MMN',1)
       ,('descomp1-MMN',2),('descomp3-MMN',2),('descomp4-MMN',2),('descomp5-MMN',2)
       ,('descomp6-MMN',2),('descomp7-MMN',2)]


# lnames=[('control8-MMN',0),('control9-MMN',0),('control10-MMN',0)
#        ,('comp2-MMN',1),('comp8-MMN',1),('comp9-MMN',1)
#        ,('descomp10-MMN',2),('comp12-MMN',2)]


#lnames=['comp10-MEG','comp12-MEG','comp10-MMN','comp12-MMN']
#lcol=[1,1,1,1]
#lband=['alpha','beta','gamma-l','gamma-h','theta','delta','gamma-h']
lband=['all', 'gamma-l', 'gamma-h']
badchannels=['A53', 'A31', 'A94']
for band in lband:
    examps=None
    print band,
    lcol = []
    for name,cl in lnames:
        print name,
        lcol.append(cl)
        mats = scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
        data = mats['data']
        chann = mats['names']
    
        j=0
        mdata=None
        lsnames=[]
        for i in range(chann.shape[0]):
            cname=chann[i][0][0]
            if cname[0]=='A' and not cname in badchannels:
                j+=1
                lsnames.append(cname)
                if mdata==None:
                    mdata=data[i]
                else:
                    mdata=np.vstack((mdata,data[i]))
            else:
                print cname,i
        cmatrix = correlationMatrix(mdata,0,mdata.shape[1],10)
        examp = np.zeros((j*(j-1)/2))
        
        p=0
        for i in range(cmatrix.shape[0]-1):
            for j in range(i+1,cmatrix.shape[0]):
                examp[p] = cmatrix[i,j]
                p += 1
                
        if examps==None:
            examps=examp
        else:
            examps=np.vstack((examps,examp))
    
    X=examps
    Y=np.array(lcol)
    patdata={}
    patdata['data']=X
    patdata['classes']=Y
    scipy.io.savemat(cres+'patcov-train-'+band,patdata,do_compression=True)
#    scipy.io.savemat(cres+'patcorr-new',patdata,do_compression=True)
    print

