"""
.. module:: MEGClassify

MEGClassify
*************

:Description: MEGClassify

    

:Authors: bejar
    

:Version: 

:Created on: 09/09/2014 11:42 

"""

__author__ = 'bejar'

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
from sklearn.cross_validation import LeaveOneOut
from scipy import corrcoef
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from sklearn.decomposition import PCA,KernelPCA

cpath='/home/bejar/Copy/MEG/Correlation/'


#name='control1-MMN'
patdata=scipy.io.loadmat(cpath+'patcov-train-gamma-h.mat')

X = patdata['data']
Y = patdata['classes'].ravel()
for i in range(Y.shape[0]):
    if Y[i] == 2:
        Y[i] = 1
loo = LeaveOneOut(X.shape[0])

mms = MinMaxScaler()

mms.fit(X)
X = mms.transform(X)

print loo

for train,test in loo:
    svm = SVC(C=10000)
    X_train = X[train]
    Y_train = Y[train]
    X_test = X[test]
    Y_test = Y[test]
    svm.fit(X_train,Y_train)
    print svm.score(X_test,Y_test)
