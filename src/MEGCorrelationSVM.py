# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:12:48 2013

@author: bejar
"""

import scipy.io
import numpy as np
from scipy import corrcoef
from sklearn.cluster import spectral_clustering,affinity_propagation
import matplotlib.pyplot as plt
from pylab import *
from sklearn.metrics import silhouette_score
from sklearn.manifold import spectral_embedding
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
import pylab as pl

from scipy import corrcoef

from sklearn.decomposition import PCA,KernelPCA



def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    for length in range(linit,lend,lstep):
        corrs=corrcoef(mdata[:,length:length+lstep])
        corr+=corrs    
    corr/=nstep
    return corr

def exampleData(name):
    mats=scipy.io.loadmat( cpath+name+'.mat')
    data= mats['data']
    chann= mats['names']

    j=0
    mdata=None
    lch=[]
    for i in range(chann.shape[0]):
        cname=chann[i][0][0]
        if cname[0]=='A' and cname!='A53' and cname!='A31' and cname!='A44' and cname!='A94':
            j+=1
            if mdata==None:
                mdata=data[i]
            else:
                mdata=np.vstack((mdata,data[i]))
            lch.append(cname)
    print sort(lch)
    cmatrix=correlationMatrix(mdata,0,400000,10)
    examp=np.zeros((j*(j-1)/2))
    print j
    p=0
    for i in range(cmatrix.shape[0]-1):
        for j in range(i+1,cmatrix.shape[0]):
            #if np.isnan(corr[i,j]) or corr[i,j]<0.7:
            examp[p]=cmatrix[i,j]
            p+=1
    return examp


cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
#name='MMN-201205251030'

name='control1-MMN'
mats=scipy.io.loadmat( cres+'patcorr.mat')
data= mats['data']
cl=mats['classes']
classes=[]
for i in range(cl.shape[0]):
    classes.append(cl[i][0])
classes =np.array(classes)
lcol=cl
X=data
Y=classes


#for c in [0.001,0.01,0.1,1,10,100]:
#        clf = SVC(C=c,kernel='linear')
#        score=cross_val_score(clf,X,Y,cv=10)
#        print c,':',np.mean(score),np.std(score)
#        
#for c in [0.001,0.01,0.1,1,10,100,1000,10000]:
#    clf = SVC(C=c,kernel='linear')
#    clf.fit(X,Y)
#    #print clf.n_support_
#    print clf.predict(X)


examps=X

trans=PCA(n_components=3)

trans.fit(examps)

X=trans.transform(examps)
#X=examps
#Y=np.array(lcol)
#patdata={}
#patdata['data']=X
#patdata['classes']=Y
#scipy.io.savemat(cres+'patcorr',patdata,do_compression=True)

ax=pl.subplot(1, 1, 1, projection='3d')

pl.scatter(X[:,0],X[:,1],zs=X[:,2],c=lcol,s=25)

pl.show()

#c=1
#clf = SVC(C=c,kernel='linear',probability=True)
#clf.fit(X,Y)
#
#val=exampleData('comp10-MEG')
#
#print clf.predict(val), clf.predict_proba(val)
#
#val=exampleData('comp10-MMN')
#print clf.predict(val), clf.predict_proba(val)
