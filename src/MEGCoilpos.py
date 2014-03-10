# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 09:23:42 2013

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

cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
#name='MMN-201205251030'

name='sensorpos'
mats=scipy.io.loadmat( cpath+name+'.mat')

data= mats['chanpos']
l= mats['label']

llabels=[]
mpos=None
for i in range(l.shape[0]):
    cname=l[i][0][0]
    if cname[0]=='A':
        llabels.append(cname)
        if mpos==None:
            mpos=data[i]
        else:
            mpos=np.vstack((mpos,data[i]))

X=mpos
fig = plt.figure()
ax = fig.gca(projection='3d')

#ax=pl.subplot(1, 1, 1, projection='3d')

pl.scatter(X[:,1],X[:,2],zs=X[:,0],s=25)
for i,lab in list(enumerate(llabels)):
    print i, lab
    ax.text(X[i,1],X[i,2],X[i,0],lab,'x')


pl.show()
