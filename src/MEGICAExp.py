# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:36:11 2013

@author: bejar
"""

import scipy.io
import numpy as np
from pylab import *
from sklearn.decomposition import FastICA
from scipy import corrcoef
import heapq
from  matplotlib.backends.backend_pdf import PdfPages

def signalIndex(sig):
    ind=0
    for i in range(chann.shape[0]):
        if chann[i][0][0]==sig:
            ind=i
    return ind

def correlationMatrix(linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((data.shape[0],data.shape[0]))
    for length in range(linit,lend,lstep):
        corrs=corrcoef(data[:,length:length+lstep])
        corr+=corrs    
    corr/=nstep
    return corr

def getNeighbors(corr,nneigh,signal):
    nneighbors =  [] 

    for j in range(corr.shape[0]):  
        if signal!=j and corr[signal,j]>0.5:
          if len(nneighbors)<nneigh:
                heapq.heappush(nneighbors,(corr[signal,j],j))
          else:
                heapq.heappushpop(nneighbors,(corr[signal,j],j)) 

    return nneighbors
    
    
# The C_i^m part of the approximate entropy
def Cmi(signal,i,m,r):
    count=0.0
    for n in range(len(signal)-m):
        dist=np.amax(np.absolute(signal[i:i+m-1]-signal[n:n+m-1]))
        if dist<r:
            count+=1.0
    return count/(len(signal)-m)
    
# Computes the approximate entropy of a signal
def approximateEntropy(signal,m,thres):
    vres=0
    for i in range(len(signal)-m):
        cm=Cmi(signal,i,m,thres)
        cml=Cmi(signal,i,m+1,thres)
        vres+=np.log(cm/cml)
    return vres/(len(signal)-m)    
    
def plotSignals(signals,n,m):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    i=1
    for s in range(signals.shape[1]):
        signal1=signals[:,s]
        minaxis=min(signal1)
        maxaxis=max(signal1)
        num=len(signal1)    
        sp1=fig.add_subplot(n,m,i)
        sp1.axis([0,num,minaxis,maxaxis])
        t = arange(0.0, num, 1)   
        sp1.plot(t,signal1)
        i+=1
#    fig.savefig(pp, orientation='landscape',format='pdf')
    plt.show()   
    
def plotOneSignal(signal):
    fig = plt.figure()
    minaxis=min(signal)
    maxaxis=max(signal)
    num=len(signal)    
    sp1=fig.add_subplot(111)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,signal)
    plt.show()     
    

cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
#name='MMN-201205251030'
name='descomp3-MEG'
mats=scipy.io.loadmat( cpath+name+'.mat')
data= mats['data']
chann=mats['names']

cmatrix=correlationMatrix(0,400000,10)

sig=signalIndex('A83')
numnb=6

neigh=getNeighbors(cmatrix,numnb,sig)

print  [chann[v][0][0] for _,v in neigh]


sel=[]
sel.append(sig)
sel.extend([v for i,v in neigh])

print len(sel)

dbuffer=data[sel,0:67817]
    
fica=FastICA(n_components=len(sel),algorithm='deflation',fun='exp',max_iter=2000)

res=fica.fit_transform(dbuffer.transpose())

plotSignals(res,len(sel),1)

#temp= rfft(res[:,1])
#
#temp[0:6000]=0
#temp[12000:len(temp)-1]=0
#
#vals= irfft(temp)
#
#plotOneSignal(vals)

for i in range(res.shape[1]):
    print approximateEntropy(res[0:3000,i],2,0.001)