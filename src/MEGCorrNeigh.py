# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 14:43:50 2013

@author: bejar
"""

import scipy.io
from scipy import corrcoef
import heapq
import numpy as np


cpath='/home/bejar/MEG/Data/control/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
name='control1-MMN'
mats=scipy.io.loadmat( cpath+name+'.mat')
data= mats['data']
chann= mats['names']
linit=0
lend=400000
lstep=50000


print data.shape

corr=np.zeros((data.shape[0],data.shape[0]))
for length in range(linit,lend,lstep):
    corrs=corrcoef(data[:,length:length+lstep])
    corr+=corrs

corr/=8.0
print corr.shape

keep_size=5
nneigbors = [ [] for i in range(corr.shape[0])] 

for i in range(corr.shape[0]):
    for j in range(corr.shape[0]):  
        if i!=j and corr[i,j]>0.5:
          if len(nneigbors[i])<keep_size:
                heapq.heappush(nneigbors[i],(corr[i,j],j))
          else:
                heapq.heappushpop(nneigbors[i],(corr[i,j],j)) 

for i in range(corr.shape[0]):                                         
    print '\n',i,chann[i][0][0],':',
    for j in range(len(nneigbors[i])):
        print nneigbors[i][j][1],chann[nneigbors[i][j][1]][0][0],#nneigbors[i][j][0],
