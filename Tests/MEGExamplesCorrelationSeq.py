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

from scipy import corrcoef

from sklearn.decomposition import PCA,KernelPCA


def correlationData(mdata,linit,lend,nstep):
    
    examps=None
    lstep=(lend-linit)/nstep
    for length in range(linit,lend,lstep):
        cmatrix=corrcoef(mdata[:,length:length+lstep])
        examp=np.zeros((mdata.shape[0]*(mdata.shape[0]-1)/2))
    
        p=0
        for i in range(cmatrix.shape[0]-1):
            for j in range(i+1, cmatrix.shape[0]):
                examp[p] = cmatrix[i,j]
                p+=1
                
        if examps==None:
            examps=examp
        else:
            examps=np.vstack((examps,examp))
    

    return examps


    
cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
        ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
        ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG'
        ,'control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
        ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
        ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']
lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,5]
#[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]
#lnames=['control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
#        ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
#        ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']
#lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]
examps=None
for name in lnames:
    print name
    mats=scipy.io.loadmat( cpath+name+'.mat')
    data= mats['data']
    chann= mats['names']

    j=0
    mdata=None
#    lnames=[]
    for i in range(chann.shape[0]):
        cname=chann[i][0][0]
        if cname[0]=='A' and cname!='A53' and cname!='A31':# and cname!='A44' and cname!='A94':
            j+=1
#            lnames.append(cname)
            if mdata==None:
                mdata=data[i]
            else:
                mdata=np.vstack((mdata,data[i]))
    
    examp=correlationData(mdata,0,400000,10)
    print examp.shape    
            
    if examps==None:
        examps=examp
    else:
        examps=np.vstack((examps,examp))

print examps.shape


trans=PCA(n_components=3)

trans.fit(examps)

X=trans.transform(examps)
#X=examps
#Y=np.array(lcol)
#patdata={}
#patdata['data']=X
#patdata['classes']=Y
#scipy.io.savemat(cres+'patcorr',patdata,do_compression=True)

llcol=[]
for v in lcol:
    for r in range(10):
        llcol.append(v)
    
ax=pl.subplot(1, 1, 1, projection='3d')

pl.scatter(X[:,0],X[:,1],zs=X[:,2],c=llcol,s=25)

pl.show()
#for c in [0.01,0.1,1,10,100]:
##    for g in np.arange(0.1,1.1,0.1):
#        clf = SVC(C=c,kernel='linear')
#        score=cross_val_score(clf,X,Y,cv=10)
#        print c,':',np.mean(score),np.std(score)
#        
#clf = SVC(C=1,kernel='linear')
#clf.fit(X,Y)
#print clf.n_support_
#print clf.predict(X)
